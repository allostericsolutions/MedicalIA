import streamlit as st
from gpt_config import openai_setup
import openai

from funciones.recepcion_docs import cargar_documentos
from funciones.formulario_datos import formulario_datos
from funciones.interrogatorio_gpt import interrogatorio_gpt

def main():
    st.title("Aplicación Médica con Streamlit y OpenAI")

    openai_client = openai_setup.initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")
        modelo = "gpt-4"  # O el modelo que desees usar

        archivos = cargar_documentos() # Primero cargar archivos
        datos_biometricos = formulario_datos() # Luego obtener datos biométricos y síntomas

        if datos_biometricos:
            # Aquí procesarías los archivos y obtendrías la información relevante
            informacion_pdfs = "Información extraída de los PDFs..."  # Reemplaza con tu lógica actual
            
            # Combinar información para enviar a GPT
            informacion_completa = f"Información del paciente:\n\nBiometría: {datos_biometricos}\n\nSíntomas: {datos_biometricos['sintomas']}\n\nInformación de los PDFs: {informacion_pdfs}"

            conversacion = interrogatorio_gpt(informacion_completa, openai_client, modelo)

            # Mostrar la conversación (opcional)
            for mensaje in conversacion:
                if mensaje["role"] == "user":
                    st.write(f"👤 Usuario: {mensaje['content']}")
                else:
                    st.write(f"🤖 GPT: {mensaje['content']}")

    else:
        st.error("No se pudo inicializar el cliente de OpenAI.")

if __name__ == "__main__":
    main()
