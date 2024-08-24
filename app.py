import streamlit as st
from gpt_config import openai_setup

def main():
    st.title("Tu Aplicación de Streamlit con OpenAI")

    # Llamar a la función de inicialización de OpenAI
    openai_client = openai_setup.initialize_openai()

    if openai_client:
        # Tu lógica de la aplicación usando openai_client
        st.write("Cliente de OpenAI inicializado correctamente.")
        # Aquí puedes continuar con tu lógica usando openai_client
    else:
        # Mensaje de error si la API Key no está configurada correctamente
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
