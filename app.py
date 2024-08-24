
import streamlit as st
from gpt_config import openai_setup
import openai

def main():
    st.title("Tu Aplicación de Streamlit con OpenAI")

    # Inicializar OpenAI
    openai_client = openai_setup.initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")

        # Campo de texto para que el usuario introduzca una pregunta
        prompt = st.text_input("Haz una pregunta a GPT-3:")

        # Botón para enviar la pregunta
        if st.button("Enviar"):
            if prompt:
                # Envía la pregunta a la API de OpenAI y recibe la respuesta
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",  # Puedes cambiar por el motor que prefieras
                        prompt=prompt,
                        max_tokens=150,  # Puedes ajustar el número de tokens según tus necesidades
                        n=1,
                        stop=None,
                        temperature=0.7
                    )

                    # Muestra la respuesta en la aplicación
                    st.write(response.choices[0].text.strip())
                except Exception as e:
                    st.error(f"Ocurrió un error al obtener la respuesta: {e}")
            else:
                st.error("Por favor, introduce una pregunta.")
    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
