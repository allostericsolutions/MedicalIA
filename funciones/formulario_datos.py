import streamlit as st

def formulario_datos():
    st.header("Formulario de Datos del Paciente")
    
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=200.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=0.0, max_value=250.0, step=0.1)
    
    if st.button("Enviar Datos"):
        st.session_state.datos_paciente = {"edad": edad, "peso": peso, "altura": altura}
        return st.session_state.datos_paciente
    return None

def calcular_imc(peso, altura):
    if altura > 0:
        altura_m = altura / 100
        imc = peso / (altura_m ** 2)
        if imc < 18.5:
            categoria = "bajo peso"
        elif 18.5 <= imc < 24.9:
            categoria = "peso normal"
        elif 25 <= imc < 29.9:
            categoria = "sobrepeso"
        else:
            categoria = "obesidad"
        return imc, categoria
    else:
        return None, None
