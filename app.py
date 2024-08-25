import streamlit as st
from gpt_config import openai_setup
import openai

# Importar las nuevas funciones
from funciones.recepcion_docs import cargar_documentos
from funciones.formulario_datos import formulario_datos, calcular_imc
from funciones.interrogatorio_gpt import iniciar_conversacion, manejar_conversacion, mostrar_resumen

def main():
    st.title("Aplicación Médica con Streamlit y OpenAI")

    # La inicialización de OpenAI ya está configurada por ti.
    openai_client = openai_setup.initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")

        # Especificar el modelo de OpenAI (modificar aquí si es necesario cambiar el modelo)
        modelo = "gpt-4o-mini"

        archivos = cargar_documentos()

        if archivos:
            if "datos_paciente" not in st.session_state:
                datos_paciente = formulario_datos()
                if datos_paciente:
                    st.session_state.datos_paciente = datos_paciente

                    # Calcular y mostrar IMC
                    imc, imc_categoria = calcular_imc(datos_paciente['peso'], datos_paciente['altura'])
                    st.session_state.imc = imc
                    st.session_state.imc_categoria = imc_categoria

                    st.write(f"Tu IMC es {imc:.2f}, lo cual se considera {imc_categoria}.")
            else:
                st.write(f"Datos del paciente:")
                st.write(f"Edad: {st.session_state.datos_paciente['edad']} años")
                st.write(f"Peso: {st.session_state.datos_paciente['peso']} kg")
                st.write(f"Altura: {st.session_state.datos_paciente['altura']} cm")
                st.write(f"IMC: {st.session_state.imc:.2f} ({st.session_state.imc_categoria})")

                if "sintomas" not in st.session_state:
                    st.write("Por favor, ingresa tus síntomas:")
                    sintomas = st.text_area("")
                    if st.button("Enviar Síntomas"):
                        st.session_state.sintomas = sintomas
                        st.session_state.conversation = iniciar_conversacion(st.session_state.datos_paciente, sintomas)
                        st.experimental_rerun()

                if "sintomas" in st.session_state:
                    manejar_conversacion(openai_client, modelo)

                if st.session_state.get("mostrar_resumen"):
                    mostrar_resumen()

    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
