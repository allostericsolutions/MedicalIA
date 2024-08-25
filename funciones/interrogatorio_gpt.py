import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # Cargar el prompt y añadir datos del paciente
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()
    prompt += f"\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\n" 

    # ---->>>  Contenedor para el chat  <<<<-----
    chat_container = st.container()

    # ---->>>  Obtener Síntomas del Usuario  <<<<-----
    st.write("¿Cuáles son tus síntomas?")
    sintomas = st.text_area("", key="sintomas_input")

    if st.button("Enviar Síntomas") or (st.session_state.get("sintomas_enviados", False) and sintomas):
        st.session_state.sintomas_enviados = True

        # Añadir síntomas al prompt
        prompt += f"Síntomas: {sintomas}\n"

        # ---->>>  Inicializar la conversación  <<<<-----
        conversation = [{"role": "system", content: prompt}]
        st.session_state.conversation = conversation

    if st.session_state.get("sintomas_enviados", False):
        # ---->>>  Manejar la entrada del usuario  <<<<-----
        user_input = st.text_area("Tú:", key="user_input")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            user_input = ""  # Limpiar el área de texto

        # ---->>>  Generar respuesta de GPT  <<<<-----
        if st.session_state.conversation:
            with chat_container:
                for message in st.session_state.conversation:
                    if message["role"] == "user":
                        st.write("👤 Usuario:", message["content"]) # Mostrar mensaje del usuario
                    else:
                        st.write("🤖 GPT:", message["content"]) # Mostrar mensaje de GPT

            response = openai_client.chat.completions.create(
                model=modelo,
                messages=st.session_state.conversation
            )
            message = response.choices[0].message.content
            st.session_state.conversation.append({"role": "assistant", "content": message})

            # ---->>>  Mostrar la respuesta de GPT  <<<<-----
            with chat_container:
                st.write("🤖 GPT:", message) 

        # ---->>>  Mostrar resumen de síntomas (sin recomendaciones)  <<<<-----
        st.write("Resumen de síntomas:")
        st.write(sintomas)
