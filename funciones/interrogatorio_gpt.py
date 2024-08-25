import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt (NO se envía a GPT en la conversación)
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Contenedor para el chat
    chat_container = st.container()

    # Obtener Síntomas del Usuario (solo la primera vez)
    if "sintomas" not in st.session_state:
        st.write("¿Cuáles son tus síntomas?")
        sintomas = st.text_area("", key="sintomas_input")

        if st.button("Enviar Síntomas") or sintomas:
            st.session_state.sintomas = sintomas
    else:
        sintomas = st.session_state.sintomas

    # Inicializar la conversación (solo la primera vez)
    if "conversation" not in st.session_state:
        prompt_inicial = f"{prompt}\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\nSíntomas: {sintomas}\n"
        st.session_state.conversation = [{"role": "system", "content": prompt_inicial}]
        
        # Obtener y mostrar el primer mensaje de GPT
        response = openai_client.chat.completions.create(
            model=modelo,
            messages=st.session_state.conversation
        )
        message = response.choices[0].message.content
        st.session_state.conversation.append({"role": "assistant", "content": message})

        with chat_container:
            st.write("🤖 GPT:", message)

    # Manejar la conversación
    if st.session_state.get("conversation"):
        with chat_container:
            for message in st.session_state.conversation:
                if message["role"] == "user":
                    st.write("👤 Usuario:", message["content"])
                else:
                    st.write("🤖 GPT:", message["content"])

        # Input del usuario DENTRO del bucle
        user_input = st.text_area("Tú:", key="user_input")
        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Obtener la respuesta de GPT
            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content  # Obtener el contenido de la respuesta
            st.session_state.conversation.append({"role": "assistant", "content": message})

            # Mostrar el nuevo mensaje de GPT
            with chat_container:
                st.write("🤖 GPT:", message) 

        # Mostrar resumen de síntomas (cuando GPT lo indique)
        if "resumen de síntomas:" in message.content.lower():  # Acceder al atributo content
            st.write("Resumen de síntomas:")
            st.write(sintomas) 
