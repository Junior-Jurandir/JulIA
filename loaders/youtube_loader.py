import io
import os
import yt_dlp
from langchain_community.document_loaders import YoutubeLoader
import streamlit as st


def load_transcript(url):
    # Configurações do yt-dlp
    ydl_opts = {
        "format": "best",
        "noplaylist": True,
        "quiet": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["pt", "en"],
        "outtmpl": "%(id)s.%(ext)s",
    }

    # Usando yt-dlp para obter informações do vídeo
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get("title", None)
        author = info_dict.get("uploader", None)
        published = info_dict.get("upload_date", None)
        description = info_dict.get("description", None)
        length = info_dict.get("duration", None)
        video_id = info_dict.get("id", None)

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
