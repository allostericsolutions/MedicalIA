# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai, test_openai_connection

st.title("Configuración de OpenAI en Streamlit")

# Inicializar OpenAI
openai = initialize_openai()

if openai:
    st.success("OpenAI API configurada correctamente.")
    
    # Probar la conexión a OpenAI
    st.header("Prueba de conexión a OpenAI")
    respuesta_prueba = test_openai_connection()
    if "Error" in respuesta_prueba:
        st.error(respuesta_prueba)
    else:
        st.success("Conexión a OpenAI exitosa.")
        st.write(f"Respuesta de prueba: {respuesta_prueba}")
