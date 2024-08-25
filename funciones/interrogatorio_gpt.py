import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):  # Agrega 'modelo' como argumento
    st.header("Interrogatorio Médico con GPT")

    # Prompt inicial desde el archivo gpt_config/prompt.txt
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Añadir los datos del paciente al prompt
    prompt += f"\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\nSíntomas: {datos_paciente['sintomas']}\n"

    # Enviar el prompt a GPT-3 y obtener la respuesta
    try:
        response = openai.ChatCompletion.create(
            model=modelo,  # Utiliza el argumento 'modelo' aquí
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Haz un interrogatorio médico basado en los síntomas dados."},
            ]
        )
        
        interrogatorio = response['choices'][0]['message']['content']
        st.write("Preguntas generadas por GPT:")
        st.write(interrogatorio)

        # Recolección de respuestas a las preguntas generadas por GPT
        respuestas = st.text_area("Responde las preguntas generadas por GPT aquí:")
        
        return respuestas

    except Exception as e:
        st.error(f"Ocurrió un error al obtener el interrogatorio de GPT: {e}")
        return None
