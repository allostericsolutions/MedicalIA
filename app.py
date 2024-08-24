# gpt_config/openai_setup.py
import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de los secretos de Streamlit."""
    try:
        OPENAI_API_KEY = st.secrets["openai"]["api_key"]
        # Configura la API Key de OpenAI
        openai.api_key = OPENAI_API_KEY
        st.info("OpenAI API Key successfully retrieved from Streamlit secrets.")
        return openai
    except KeyError:
        st.error("Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai

# Inicializar OpenAI
openai = initialize_openai()

st.title("Ejemplo de Configuración de OpenAI en Streamlit")
st.write("OpenAI API configurada correctamente.")
