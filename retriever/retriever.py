import os
import tempfile
import json
import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def config_retriever(uploads):
    # Carregar documentos
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploads:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        # Handle different file types
        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(temp_filepath)
            docs.extend(loader.load())
        elif file.name.endswith(".txt"):
            with open(temp_filepath, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(
                    Document(page_content=content, metadata={"source": file.name})
                )
        elif file.name.endswith(".md"):
            with open(temp_filepath, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(
                    Document(page_content=content, metadata={"source": file.name})
                )
        elif file.name.endswith(".json"):
            with open(temp_filepath, "r", encoding="utf-8") as f:
                content = json.load(f)
                docs.append(
                    Document(page_content=str(content), metadata={"source": file.name})
                )
        elif file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(temp_filepath)
            for index, row in df.iterrows():
                docs.append(
                    Document(
                        page_content=row.to_string(),
                        metadata={"source": file.name, "page": index + 1},
                    )
                )

    # Divisão em pedaços de texto / split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

    # Armazenamento
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local("vectorstore/db_faiss")

    # Configuração do retriever
    retriever = vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "fetch_k": 4}
    )
    return retriever
