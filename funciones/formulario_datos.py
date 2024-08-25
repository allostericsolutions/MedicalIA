# funciones/formulario_datos.py
import streamlit as st

def formulario_datos():
    st.header("Datos Biométricos del Paciente")

    edad = st.number_input("Edad:", min_value=0, max_value=120, step=1)
    peso = st.number_input("Peso (kg):", min_value=0.0, max_value=300.0, step=0.1)
    talla = st.number_input("Talla (cm):", min_value=0.0, max_value=250.0, step=0.1)
    sintomas = st.text_area("Síntomas:")

    datos = {
        "edad": edad,
        "peso": peso,
        "talla": talla,
        "sintomas": sintomas
    }

    return datos
