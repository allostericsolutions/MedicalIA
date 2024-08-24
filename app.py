import streamlit as st
import gpt_config.openai_setup as openai_setup

# Inicializar OpenAI
openai_client = openai_setup.initialize_openai()

# Función para enviar mensajes a la API y obtener la respuesta
def enviar_mensaje(prompt):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,  # Ajuste el número de tokens si lo necesitas
        temperature=0.7,  # Ajuste la temperatura para controlar la aleatoriedad de las respuestas
    )
    return response.choices[0].message.content

# Título de la aplicación
st.title("ChatBot con OpenAI")

# Inicializar el historial de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar la ventana de chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Obtener la pregunta del usuario
if prompt := st.chat_input("Escribe tu mensaje:"):
    # Agregar la pregunta al historial de chat
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Obtener la respuesta del chatbot
    response = enviar_mensaje(prompt)

    # Agregar la respuesta al historial de chat
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Mostrar la respuesta en la ventana de chat
    with st.chat_message("assistant"):
        st.write(response)
