# gpt_config/openai_setup.py
import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de Streamlit Secrets."""
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    openai.api_key = OPENAI_API_KEY
    return openai.OpenAI()

def test_openai_connection():
    """Prueba la conexión con OpenAI haciendo una consulta simple."""
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="¿Cuál es la capital de Francia?",
            max_tokens=10
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"
