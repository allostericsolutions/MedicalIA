import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Prompt inicial desde el archivo gpt_config/prompt.txt
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Añadir los datos del paciente al prompt
    prompt += f"\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\nSíntomas: {datos_paciente['sintomas']}\n"

    # Enviar el prompt a GPT y obtener la respuesta
    try:
        response = openai_client.chat.completions.create( # Actualización para OpenAI >= 1.0.0
            model=modelo,  # Usa el modelo apropiado
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Haz un interrogatorio médico basado en los síntomas dados. Presenta las preguntas una a una."},
            ]
        )
        
        interrogatorio = response.choices[0].message.content # Actualización para OpenAI >= 1.0.0
        st.write("Preguntas generadas por GPT:")
        st.write(interrogatorio)

        # Separar las preguntas para presentarlas individualmente
        preguntas = interrogatorio.split("\n")

        # Mostrar cada pregunta en una ventana de diálogo separada
        respuestas = []
        for pregunta in preguntas:
            if pregunta.strip():  # Ignorar líneas vacías
                respuesta = st.text_area(pregunta)
                respuestas.append(respuesta)

        # Una vez que el usuario ha respondido todas las preguntas
        # Enviar las respuestas a GPT para obtener la respuesta final
        prompt_final = f"Las respuestas del paciente son: \n{'\n'.join(respuestas)}\n\nBasándose en esta información, ¿cuál es tu diagnóstico y recomendaciones para el paciente?"

        response_final = openai_client.chat.completions.create( # Actualización para OpenAI >= 1.0.0
            model=modelo,  # Utilizar el mismo modelo que antes
            messages=[
                {"role": "system", "content": prompt_final},
            ]
        )

        respuesta_gpt = response_final.choices[0].message.content # Actualización para OpenAI >= 1.0.0
        st.write("Respuesta de GPT:")
        st.write(respuesta_gpt)

        return respuestas

    except Exception as e:
        st.error(f"Ocurrió un error al obtener el interrogatorio de GPT: {e}")
        return None
