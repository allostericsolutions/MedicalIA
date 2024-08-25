import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Inicializar la conversación si aún no se ha hecho
    if "conversation" not in st.session_state:
        if 'edad' in datos_paciente and 'peso' in datos_paciente and 'altura' in datos_paciente and \
            isinstance(datos_paciente['edad'], (int, float)) and \
            isinstance(datos_paciente['peso'], (int, float)) and \
            isinstance(datos_paciente['altura'], (int, float)):
            
            prompt_inicial = f"{prompt}\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nAltura: {datos_paciente['altura']} cm\n\nHola, ¿podrías contarme cuáles son tus síntomas?"
            st.session_state.conversation = [{"role": "system", "content": prompt_inicial}]
        else:
            st.error("Datos del paciente incompletos o inválidos.")
            return

    # Mostrar la conversación
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.conversation:
            if message["role"] == "user":
                st.write("👤 Usuario:", message["content"])
            else:
                st.write("🤖 GPT:", message["content"])

        # Entrada del usuario
        user_input = st.text_area("Escribe aquí tus síntomas:", key="user_input")
        if st.button("Enviar"):
            if user_input:
                st.session_state.conversation.append({"role": "user", "content": user_input})

                response = openai_client.chat_completions.create(
                    model=modelo,
                    messages=st.session_state.conversation
                )
                message = response.choices[0].message["content"]
                st.session_state.conversation.append({"role": "assistant", "content": message})
                st.write("🤖 GPT:", message)

    return st.session_state.conversation
