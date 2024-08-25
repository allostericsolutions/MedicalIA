import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Contenedor para el chat
    chat_container = st.container()

    # Inicializar la conversación (SOLO si no existe)
    if "conversation" not in st.session_state:
        prompt_inicial = f"{prompt}\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nAltura: {datos_paciente['altura']} cm\n\nHola, ¿podrías contarme cuáles son tus síntomas?" 
        st.session_state.conversation = [{"role": "system", "content": prompt_inicial}]

    # Manejar la conversación (esta parte siempre se ejecuta)
    with chat_container:
        for message in st.session_state.conversation:
            if message["role"] == "user":
                st.write("👤 Usuario:", message["content"])
            else:
                st.write("🤖 GPT:", message["content"])

        user_input = st.text_area("Tú:", key="user_input")
        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})

            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content
            st.session_state.conversation.append({"role": "assistant", "content": message})

            st.write("🤖 GPT:", message)

    return st.session_state.conversation
