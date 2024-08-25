import streamlit as st
from gpt_config import openai_setup
import openai

# Importar las nuevas funciones
from funciones.recepcion_docs import cargar_documentos
from funciones.formulario_datos import formulario_datos
from funciones.interrogatorio_gpt import interrogatorio_gpt

def main():
    st.title("Aplicación Médica con Streamlit y OpenAI")

    # La inicialización de OpenAI ya está configurada por ti.
    openai_client = openai_setup.initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")

        # Especificar el modelo de OpenAI 
        modelo = "gpt-4"

        # Cargar archivos primero
        archivos = cargar_documentos()

        # Luego obtener datos del paciente
        datos_paciente = formulario_datos()  

        if datos_paciente:
            if archivos:
                st.write("Archivos cargados y datos del paciente recopilados.")
                st.write(datos_paciente)

                # Interrogatorio médico con GPT
                respuestas_interrogatorio = interrogatorio_gpt(datos_paciente, openai_client, modelo)

                if respuestas_interrogatorio:
                    # Mostrar cada mensaje en la conversación
                    for mensaje in respuestas_interrogatorio:
                        if mensaje["role"] == "user":
                            st.write(f"👤 Usuario: {mensaje['content']}")
                        else:
                            st.write(f"🤖 GPT: {mensaje['content']}")

    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
