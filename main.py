# Importações
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
import glob
from langchain_community.document_loaders import YoutubeLoader
import yt_dlp
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import json
import torch
from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub
from langchain_core.documents import Document
import faiss
import io
import tempfile
import os
import time
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import YoutubeLoader, PyPDFLoader
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Definir pasta padrão para uploads automáticos
UPLOAD_FOLDER = "uploads"

# Configurações do Streamlit
st.set_page_config(page_title="JulIA 🖥️", page_icon="🖥️")
st.title("JulIA 🖥️")

# Função para carregar a transcrição do YouTube
def load_transcript(url):
    # Configurações do yt-dlp
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['pt', 'en'],
        'outtmpl': '%(id)s.%(ext)s',
    }

    # Usando yt-dlp para obter informações do vídeo
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
        author = info_dict.get('uploader', None)
        published = info_dict.get('upload_date', None)
        description = info_dict.get('description', None)
        length = info_dict.get('duration', None)
        video_id = info_dict.get('id', None)

    # Pegando a Transcrição
    video_loader = YoutubeLoader.from_youtube_url(url, language=["pt", "pt-BR", "en"])
    infos = video_loader.load()
    transcricao = infos[0].page_content

    # Montando as informações do vídeo
    infos_video = f"""Informações sobre o vídeo:

    Título: {title}
    Autor: {author}
    Data: {published}
    Descrição: {description}
    Duração: {length}
    URL: https://www.youtube.com/watch?v={video_id}

    Transcrição: {transcricao}
    """

    # Salvando a transcrição em um arquivo
    filename = title + ".txt"
    with io.open(filename, "w", encoding="utf-8") as f:
        for doc in infos:
            f.write(infos_video)

    # Adiciona o arquivo gerado à lista de uploads
    with open(filename, "rb") as f:
        file_data = f.read()
        file_obj = io.BytesIO(file_data)
        file_obj.name = filename
        if "uploads" not in st.session_state:
            st.session_state.uploads = []
        st.session_state.uploads.append(file_obj)

# Funções para carregar modelos
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    llm = HuggingFaceHub(
        repo_id=model,
        model_kwargs={
            "temperature": temperature,
            "return_full_text": False,
            "max_new_tokens": 2048,
        }
    )
    return llm

def model_openai(model="gpt-4o-mini", temperature=0.1):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature
    )
    return llm

def model_ollama(model="phi3", temperature=0.1):
    llm = ChatOllama(
        model=model,
        temperature=temperature,
    )
    return llm

# Função para configurar o retriever
def config_retriever(uploads):
    # Carregar documentos
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploads:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        # Handle different file types
        if file.name.endswith('.pdf'):
            loader = PyPDFLoader(temp_filepath)
            docs.extend(loader.load())
        elif file.name.endswith('.txt'):
            with open(temp_filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append(Document(page_content=content, metadata={"source": file.name}))
        elif file.name.endswith('.md'):
            with open(temp_filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append(Document(page_content=content, metadata={"source": file.name}))
        elif file.name.endswith('.json'):
            with open(temp_filepath, 'r', encoding='utf-8') as f:
                content = json.load(f)
                docs.append(Document(page_content=str(content), metadata={"source": file.name}))
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(temp_filepath)
            for index, row in df.iterrows():
                docs.append(Document(page_content=row.to_string(), metadata={"source": file.name, "page": index+1}))

    # Divisão em pedaços de texto / split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

    # Armazenamento
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local('vectorstore/db_faiss')

    # Configuração do retriever
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 3, 'fetch_k': 4})
    return retriever

def load_files_from_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    files = glob.glob(os.path.join(UPLOAD_FOLDER, "*"))
    for file_path in files:
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_obj = io.BytesIO(file_data)
            file_obj.name = os.path.basename(file_path)
            if "uploads" not in st.session_state:
                st.session_state.uploads = []
            st.session_state.uploads.append(file_obj)

# Função para configurar a chain
def config_rag_chain(model_class, retriever):
    # Carregamento da LLM
    if model_class == "hf_hub":
        llm = model_hf_hub()
    elif model_class == "openai":
        llm = model_openai()
    elif model_class == "ollama":
        llm = model_ollama()

    # Definição dos prompts
    if model_class.startswith("hf"):
        token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    else:
        token_s, token_e = "", ""

    # Prompt de contextualização
    context_q_system_prompt = "Given the following chat history and the follow-up question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    context_q_system_prompt = token_s + context_q_system_prompt
    context_q_user_prompt = "Question: {input}" + token_e
    context_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", context_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", context_q_user_prompt),
        ]
    )

    # Chain para contextualização
    history_aware_retriever = create_history_aware_retriever(llm=llm, retriever=retriever, prompt=context_q_prompt)
    
    # Prompt para perguntas e respostas (Q&A)
    qa_prompt_template = """Você é a JulIA um assistente virtual prestativo focado em suporte técnico e está respondendo perguntas gerais sobre o ambiente técnico da empresa.
    Use os seguintes pedaços de contexto recuperado para responder à pergunta.
    Você foi criada pelo Jurandir Batista de Souza Junior.
    Se você não sabe a resposta, apenas diga que não sabe. 
    Sempre responda em português. \n\n
    Pergunta: {input} \n
    Contexto: {context}"""

    qa_prompt = PromptTemplate.from_template(token_s + qa_prompt_template + token_e)

    # Configurar LLM e Chain para perguntas e respostas (Q&A)
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain

# Interface do Streamlit

# Adiciona uma lista suspensa para selecionar o modelo
model_class = st.sidebar.selectbox(
    "Selecione o provedor do modelo:",
    ["hf_hub", "openai", "ollama"]
)

# Criação de painel lateral na interface
video_url = st.sidebar.text_input("Insira a URL do vídeo do YouTube:")
if video_url:
    if st.sidebar.button("Carregar Transcrição"):
        try:
            load_transcript(video_url)
            st.sidebar.success("Transcrição carregada com sucesso!")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar transcrição: {str(e)}")

# Carrega arquivos da pasta de uploads automaticamente
load_files_from_folder()

# Inicializa uploads com arquivos da sessão, se existirem
if "uploads" not in st.session_state:
    st.session_state.uploads = []

uploads = st.sidebar.file_uploader(
    label="Enviar arquivos", type=["pdf", "txt", "xls", "xlsx", "md", "json"],
    accept_multiple_files=True
)

# Combina uploads atuais com arquivos da sessão
if uploads:
    st.session_state.uploads.extend(uploads)

if not st.session_state.uploads:
    st.info("Por favor, envie algum arquivo para continuar")
    st.stop()

# Inicializa histórico de chat e retriever na sessão
if "chat_history" not in st.session_state:
    st.session_state.feedback_data = []
    st.session_state.chat_history = [
        AIMessage(content="Olá, me chamo JulIA, como posso ajudar?", sender="JulIA"),
    ]

if "docs_list" not in st.session_state:
    st.session_state.docs_list = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Exibe histórico de chat
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Processa entrada do usuário
start = time.time()
user_query = st.chat_input("Digite sua mensagem aqui...")

if user_query is not None and user_query != "" and uploads is not None:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        if st.session_state.docs_list != st.session_state.uploads:
            st.session_state.docs_list = st.session_state.uploads
            st.session_state.retriever = config_retriever(st.session_state.uploads)
        
        rag_chain = config_rag_chain(model_class, st.session_state.retriever)

        result = rag_chain.invoke({"input": user_query, "chat_history": st.session_state.chat_history, "feedback_data": st.session_state.feedback_data})

        resp = result['answer']
        st.write(resp, sender="JulIA")

        # Seção de feedback
        feedback = st.radio("A resposta foi útil?", ("Sim", "Não"))

        if feedback == "Não":
            st.write("Você selecionou 'Não'. Por favor, forneça a resposta correta:")
            correct_answer = st.text_input("Por favor, forneça a resposta correta:")
        if st.button("Enviar Feedback"):
            # Debugging: Check if feedback data is being appended
            print("Feedback submitted:", user_query, resp, feedback, correct_answer)

            # Aqui você pode armazenar o feedback e a resposta correta
            st.session_state.feedback_data.append({
                "user_query": user_query,
                "ai_response": resp,
                "feedback": feedback,
                "correct_answer": correct_answer
            })
            st.success("Obrigado pelo seu feedback!")

        # Mostrar a fonte
        sources = result['context']
        for idx, doc in enumerate(sources):
            source = doc.metadata['source']
            file = os.path.basename(source)
            page = doc.metadata.get('page', 'Página não especificada')

            # Fonte 1: documento.pdf - p. 2
            ref = f":link: Fonte {idx}: *{file} - p. {page}*"
            with st.popover(ref):
                st.caption(doc.page_content)

    st.session_state.chat_history.append(AIMessage(content=resp))

end = time.time()
print("Tempo: ", end - start)