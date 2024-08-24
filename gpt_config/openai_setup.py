import streamlit as st

def initialize_openai():
    # Verifica si 'openai' está en st.secrets
    if "openai" in st.secrets:
        # Verifica si 'api_key' está en st.secrets['openai']
        if "api_key" in st.secrets["openai"]:
            OPENAI_API_KEY = st.secrets["openai"]["api_key"]
            st.write("API Key de OpenAI cargada correctamente.")
            return OPENAI_API_KEY
        else:
            st.error("La clave 'api_key' no se encuentra en st.secrets['openai'].")
            # Imprime las claves disponibles en st.secrets['openai']
            st.write("Claves disponibles en 'openai':", list(st.secrets["openai"].keys()))
    else:
        st.error("La clave 'openai' no se encuentra en st.secrets.")
        # Imprime las claves disponibles en st.secrets
        st.write("Claves disponibles:", list(st.secrets.keys()))
    
    return None
