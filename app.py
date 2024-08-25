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

        # Especificar el modelo de OpenAI (modificar aquí si es necesario cambiar el modelo)
        modelo = "gpt-4"

        datos_paciente = formulario_datos()  # Obtener datos del paciente primero

        if datos_paciente:  # Verificar si se recibieron datos
            archivos = cargar_documentos()

            if archivos:
                st.write("Archivos cargados y datos del paciente recopilados.")
                st.write(datos_paciente)

                # Interrogatorio médico con GPT
                respuestas_interrogatorio = interrogatorio_gpt(datos_paciente, openai_client, modelo)
                
                if respuestas_interrogatorio:
                    st.write("Respuestas al interrogatorio GPT recopiladas.")
                    st.write(respuestas_interrogatorio)

                # Aquí podrías agregar lógica adicional para procesar los archivos y datos del paciente
                # y finalmente enviar a GPT o enviar por correo según sea necesario.
    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
