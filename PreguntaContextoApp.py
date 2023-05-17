import streamlit as st
import openai
from io import BytesIO
import base64
import requests
from PyPDF2 import PdfReader, PdfFileReader
from docx import Document
import re

st.set_page_config(layout="wide")

def read_pdf(pdf_file):
    reader = PdfFileReader(pdf_file)
    text = "".join(page.extract_text() for page in reader.pages)
    return text

def read_txt(txt_file):
    return txt_file.read().decode()

def read_docx(docx_file):
    document = Document(docx_file)
    text = "".join(paragraph.text for paragraph in document.paragraphs)
    return text

def read_file(file):
    extension = file.name.split(".")[-1].lower()
    if extension == "pdf":
        return read_pdf(BytesIO(file.read()))
    elif extension == "txt":
        return read_txt(BytesIO(file.read()))
    elif extension == "docx":
        return read_docx(BytesIO(file.read()))
    else:
        raise ValueError("Formato de archivo no compatible")

col1, col2 = st.beta_columns([3,7])

with col1:
    st.write("To get your openai API key, follow these steps:")
    st.write("1. Navigate to https://platform.openai.com/")
    st.write("2. Click on your avatar in the top right-hand corner of the dashboard.")
    st.write("3. Select View API Keys.")
    st.write("4. Click Create new secret key.")

with col2:
    st.title("Pregunta sobre el contenido de un archivo a GPT-3.5-turbo")

    st.subheader("Carga de Contexto")

    uploaded_contexto = st.file_uploader("Cargar Contexto (pdf, txt o docx)", type=['pdf', 'txt', 'docx'])

    api_key = st.text_input("API KEY de OpenAI")
    instruccion = st.text_input("Tomando en cuenta el contenido del archivo anterior, quiero que...")

    if uploaded_contexto and api_key and instruccion:
        contexto = read_file(uploaded_contexto)

        openai.api_key = api_key

        st.subheader("Resultado de GPT-3
