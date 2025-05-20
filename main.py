import streamlit as st
import time
import os
from langchain_core.messages import AIMessage, HumanMessage
from utils.config import UPLOAD_FOLDER
from loaders.youtube_loader import load_transcript
from loaders.file_loader import load_files_from_folder
from retriever.retriever import config_retriever
from chains.rag_chain import config_rag_chain

# Configurações do Streamlit
st.set_page_config(page_title="JulIA 🖥️", page_icon="🖥️")
st.title("JulIA 🖥️")

# Adiciona uma lista suspensa para selecionar o modelo
model_class = st.sidebar.selectbox(
    "Selecione o provedor do modelo:", ["hf_hub", "openai", "ollama"]
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
    label="Enviar arquivos",
    type=["pdf", "txt", "xls", "xlsx", "md", "json"],
    accept_multiple_files=True,
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

        result = rag_chain.invoke(
            {
                "input": user_query,
                "chat_history": st.session_state.chat_history,
                "feedback_data": st.session_state.feedback_data,
            }
        )

        resp = result["answer"]
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
            st.session_state.feedback_data.append(
                {
                    "user_query": user_query,
                    "ai_response": resp,
                    "feedback": feedback,
                    "correct_answer": correct_answer,
                }
            )
            st.success("Obrigado pelo seu feedback!")

        # Mostrar a fonte
        sources = result["context"]
        for idx, doc in enumerate(sources):
            source = doc.metadata["source"]
            file = os.path.basename(source)
            page = doc.metadata.get("page", "Página não especificada")

            # Fonte 1: documento.pdf - p. 2
            ref = f":link: Fonte {idx}: *{file} - p. {page}*"
            with st.popover(ref):
                st.caption(doc.page_content)

    st.session_state.chat_history.append(AIMessage(content=resp))

end = time.time()
print("Tempo: ", end - start)
