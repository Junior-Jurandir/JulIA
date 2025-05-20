import os
import glob
import io
import streamlit as st
from utils.config import UPLOAD_FOLDER


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
