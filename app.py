# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai

st.title("Configuración de OpenAI en Streamlit")

# Inicializar OpenAI
openai = initialize_openai()

if openai:
    st.success("OpenAI API configurada correctamente.")
