# app.py
import streamlit as st
from gpt_config import openai_setup
import openai

# Importar las nuevas funciones
from funciones.recepcion_docs import cargar_documentos
from funciones.formulario_datos import formulario_datos

def main():
    st.title("Aplicación Médica con Streamlit y OpenAI")

    # Inicializar OpenAI
    openai_client = openai_setup.initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")

        archivos = cargar_documentos()
        
        if archivos:
            datos_paciente = formulario_datos()

            st.write("Archivos cargados y datos del paciente recopilados.")
            st.write(datos_paciente)
            
            # Aquí podrías agregar lógica adicional para procesar los archivos y datos del paciente
            # y finalmente enviar a GPT o enviar por correo según sea necesario.

    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
