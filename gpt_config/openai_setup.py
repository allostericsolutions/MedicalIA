# gpt_config/openai_setup.py
import openai
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de los secretos de Streamlit."""
    OPENAI_API_KEY = st.secrets.get("openai", {}).get("api_key", None)

    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()

    # Asignar la clave API de OpenAI
    openai.api_key = OPENAI_API_KEY
    logging.info("OpenAI API Key successfully retrieved from Streamlit secrets.")
    
    return openai
