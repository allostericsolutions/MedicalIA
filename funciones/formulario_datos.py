import streamlit as st

def formulario_datos():
    st.header("Formulario de Datos del Paciente")
    
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=200.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=0.0, max_value=250.0, step=0.1)
    
    if st.button("Enviar Datos"):
        st.session_state.datos_paciente = {"edad": edad, "peso": peso, "altura": altura}
        return st.session_state.datos_paciente  # Devolver el diccionario
    return None  # Asegurarse de devolver None si no se pulsa el botón
