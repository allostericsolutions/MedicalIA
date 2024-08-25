import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt (NO se envía a GPT en la conversación)
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    # Contenedor para el chat
    chat_container = st.container()

    # Obtener Síntomas del Usuario
    st.write("¿Cuáles son tus síntomas?")
    sintomas = st.text_area("", key="sintomas_input")

    if st.button("Enviar Síntomas") or (st.session_state.get("sintomas_enviados", False) and sintomas):
        st.session_state.sintomas_enviados = True

        # Inicializar la conversación
        prompt_inicial = f"{prompt}\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\nSíntomas: {sintomas}\n"
        conversation = [{"role": "system", "content": prompt_inicial}]
        st.session_state.conversation = conversation

        # Mostrar el primer mensaje de GPT (si no se ha enviado aún)
        if len(st.session_state.conversation) == 1:  
            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content
            st.session_state.conversation.append({"role": "assistant", "content": message})

            with chat_container:
                st.write("🤖 GPT:", message) 

    if st.session_state.get("sintomas_enviados", False):
        # Manejar la entrada del usuario
        user_input = st.text_area("Tú:", key="user_input")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            user_input = ""  # Limpiar el área de texto

            # Generar respuesta de GPT (siempre que haya nueva entrada)
            with chat_container:
                for message in st.session_state.conversation:
                    if message["role"] == "user":
                        st.write("👤 Usuario:", message["content"])
                    else:
                        st.write("🤖 GPT:", message["content"])

            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content
            st.session_state.conversation.append({"role": "assistant", "content": message})

            with chat_container:
                st.write("🤖 GPT:", message) 

        # ---->>>  El resumen se mostrará cuando GPT indique que ha terminado  <<<<----- 
        # (Asegúrate de que tu prompt esté configurado para que GPT indique cuándo ha terminado)
        if "resumen de síntomas:" in message.lower(): 
            st.write("Resumen de síntomas:")
            st.write(sintomas) 
