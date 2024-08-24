# gpt_config/openai_setup.py
import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de Streamlit Secrets."""
    try:
        OPENAI_API_KEY = st.secrets["openai"]["api_key"]
    except KeyError:
        st.error("Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()
    
    # Configura la API Key de OpenAI
    openai.api_key = OPENAI_API_KEY
    
    return openai
