# gpt_config/openai_setup.py
import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de los secretos de Streamlit."""
    try:
        OPENAI_API_KEY = st.secrets["openai"]["api_key"]
        openai.api_key = OPENAI_API_KEY
        return openai
    except KeyError:
        st.error("Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()
