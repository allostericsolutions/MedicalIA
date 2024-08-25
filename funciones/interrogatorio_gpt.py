import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt (NO se envía a GPT en la conversación)
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Contenedor para el chat
    chat_container = st.container()

    # Inicializar la conversación con la pregunta inicial de GPT
    if "conversation" not in st.session_state:
        prompt_inicial = f"{prompt}\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\n\nHola, ¿podrías contarme cuáles son tus síntomas?" 
        st.session_state.conversation = [{"role": "system", "content": prompt_inicial}]
        
    # Manejar la conversación (similar a como lo hacías antes)
    if st.session_state.get("conversation"):
        with chat_container:
            for message in st.session_state.conversation:
                if message["role"] == "user":
                    st.write("👤 Usuario:", message["content"])
                else:
                    st.write("🤖 GPT:", message["content"])

        # Input del usuario
        user_input = st.text_area("Tú:", key="user_input")
        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Obtener la respuesta de GPT
            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content 
            st.session_state.conversation.append({"role": "assistant", "content": message})

            # Mostrar el nuevo mensaje de GPT
            with chat_container:
                st.write("🤖 GPT:", message) 

    # (Opcional) Devolver toda la conversación para su posterior procesamiento
    return st.session_state.conversation 
