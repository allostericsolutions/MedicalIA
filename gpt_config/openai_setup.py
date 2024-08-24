# gpt_config/openai_setup.py
import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de Streamlit Secrets."""
    try:
        OPENAI_API_KEY = st.secrets["openai"]["api_key"]
    except KeyError:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    
    # Configura la API Key y ajusta los headers para usar la versión v2 de la API
    openai.api_key = OPENAI_API_KEY
    openai.default_headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "assistants=v2"
    }
    return openai.Client()
