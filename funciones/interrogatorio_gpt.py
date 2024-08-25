import streamlit as st
import openai

def interrogatorio_gpt(datos_paciente, openai_client, modelo):
    st.header("Interrogatorio Médico con GPT")

    # ---->>>  Cargar el prompt y añadir datos del paciente  <<<<-----
    with open('gpt_config/prompt.txt', 'r') as file:
        prompt = file.read()

    prompt += f"\nDatos del paciente:\nEdad: {datos_paciente['edad']} años\nPeso: {datos_paciente['peso']} kg\nTalla: {datos_paciente['talla']} cm\n" 

    # ---->>>  Obtener Síntomas del Usuario  <<<<-----
    st.write("¿Cuáles son tus síntomas?")
    sintomas = st.text_area("", key="sintomas_input")

    # ---->>>  Botón para enviar síntomas  <<<<-----
    if st.button("Enviar Síntomas") or (st.session_state.get("sintomas_enviados", False) and sintomas):
        st.session_state.sintomas_enviados = True  # Marcar síntomas como enviados

        # ---->>> Añadir síntomas al prompt  <<<<-----
        prompt += f"Síntomas: {sintomas}\n"

        # ---->>>  Interacción con GPT  <<<<-----
        conversation = [{"role": "system", "content": prompt}]
        
        while True: 
            # Obtener la respuesta de GPT
            response = openai_client.chat.completions.create(
                model=modelo,
                messages=conversation
            )

            message = response.choices[0].message.content
            st.write("GPT: ", message)

            # Verificar si GPT ha terminado de preguntar
            if "¿algo más?" in message.lower():
                break

            # Obtener la respuesta del usuario 
            user_input = st.text_area("", key=f"user_input_{len(conversation)}")
            if st.button("Enviar", key=f"send_button_{len(conversation)}") or user_input:
                conversation.append({"role": "user", "content": user_input})

        # ---->>>  Mostrar resumen de síntomas (sin recomendaciones)  <<<<-----
        st.write("Resumen de síntomas:")
        st.write(sintomas)

    else:
        st.session_state.sintomas_enviados = False  
