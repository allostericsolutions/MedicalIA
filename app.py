# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai

# Inicializar OpenAI
openai = initialize_openai()

st.title("Ejemplo de Configuración de OpenAI en Streamlit")
st.write("OpenAI API configurada correctamente.")
