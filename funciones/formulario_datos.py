mport streamlit as st

def formulario_datos():
    st.header("Ingresa tus datos")

    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=200.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=0.0, max_value=250.0, step=0.1)
    sintomas = st.text_area("Describe tus síntomas aquí:")

    if st.button("Enviar Datos"):
        datos = {
            "edad": edad,
            "peso": peso,
            "altura": altura,
            "sintomas": sintomas
        }
        return datos
    return None
