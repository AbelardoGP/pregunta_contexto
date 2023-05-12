import streamlit as st
import openai
from io import BytesIO
import base64
import requests
from PyPDF2 import PdfReader
from docx import Document
import re

st.set_page_config(layout="wide")

def read_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        reader = PdfReader(file)
        text = "".join(page.extract_text() for page in reader.pages)
    return text

def read_txt(txt_file):
    with open(txt_file, "r") as file:
        text = file.read()
    return text

def read_docx(docx_file):
    document = Document(docx_file)
    text = "".join(paragraph.text for paragraph in document.paragraphs)
    return text

def read_file(file):
    extension = file.name.split(".")[-1].lower()
    if extension == "pdf":
        return read_pdf(file)
    elif extension == "txt":
        return read_txt(file)
    elif extension == "docx":
        return read_docx(file)
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
    st.title("Evaluación con GPT-4")

    st.subheader("Carga de Contexto")

    uploaded_contexto = st.file_uploader("Cargar Contexto (pdf, txt o docx)", type=['pdf', 'txt', 'docx'])

    api_key = st.text_input("API KEY de OpenAI")
    instruccion = st.text_input("Instrucción para GPT-3.5-turbo")

    if uploaded_contexto and api_key and instruccion:
        contexto = read_file(uploaded_contexto)

        openai.api_key = api_key

        st.subheader("Resultado de GPT-3.5 turbo")

        if st.button("Enviar a GPT-4"):
            model_engine = "gpt-3.5-turbo" # Reemplazar con el nombre del motor GPT-4 que desee utilizar
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Tomando en cuenta el archivo contexto:\n{contexto}\n\nInstrucción:\n{instruccion}"}
            ]
            response = openai.ChatCompletion.create(
                model=model_engine,
                messages=messages,
                max_tokens=900,
                n=1,
                stop=None,
                temperature=0.8,
            )
            st.write(response.choices[0].message['content'].strip())
