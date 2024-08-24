# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai

st.title("Configuración de OpenAI en Streamlit")

# Inicializar OpenAI
openai = initialize_openai()

if openai:
    st.success("OpenAI API configurada correctamente.")
    st.write(f"OpenAI Key usada: {st.secrets['openai']['api_key'][:5]}...")  # Mostrar parcialmente la key para verificar
