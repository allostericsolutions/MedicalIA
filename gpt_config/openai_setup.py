import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y obtiene la clave API de Streamlit Secrets."""
    OPENAI_API_KEY = st.secrets["openai"]["api_key"]
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()
    
    # Configura la API Key y los encabezados para usar la v2 de la API
    openai.api_key = OPENAI_API_KEY
    openai.default_headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "assistants=v2"
    }
    return openai

def test_openai_connection():
    """Prueba la conexión con OpenAI haciendo una consulta simple."""
    try:
        # Usar ChatCompletion en lugar de Completion
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": "¿Cuál es la capital de Francia?"}],
            max_tokens=10
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {e}"
