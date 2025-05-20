from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from models.hf_hub import model_hf_hub
from models.openai import model_openai
from models.ollama import model_ollama


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
        token_s, token_e = (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>",
            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
        )
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
    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=retriever, prompt=context_q_prompt
    )

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
