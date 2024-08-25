import streamlit as st
from gpt_config.openai_setup import initialize_openai
import openai
from pdfminer.high_level import extract_text
import re

# Importar funciones existentes (Asegúrate de que estos archivos existan)
from funciones.recepcion_docs import cargar_documentos
from funciones.formulario_datos import formulario_datos
from funciones.interrogatorio_gpt import interrogatorio_gpt

# Función para limpiar el texto extraído
def clean_text(raw_text):
    patterns_to_remove = [
        r"PACIENTE:.*", 
        r"\d+ de \d+", 
        r"Fecha [A-Za-z]+:.*", 
        r"Género: \w+", 
        r"Edad: \d+ Años", 
        r"No\. Orden .*", 
        r"Médico:.*", 
        r"Servicio:.*", 
        r"Campus:.*", 
        r"Instrumento:.*", 
        r"Usuario:.*", 
        r"Metodo:.*", 
        r"NOTA:.*", 
        r"Jefe de laboratorio.*", 
        r"JEFE LABORATORIO.*", 
        r"Sucursal.*", 
        r"Liberó.*", 
        r"Paciente.*", 
        r"N° Paciente.*", 
        r"interpretación deberá.*", 
        r"Página.*", 
        r"\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+.*", 
        r"\b[0-3]?\d/[0-1]?\d/\d{4}\b", 
        r"\b[0-2]?\d:[0-5]?\d:[0-5]?\d\b", 
        r"Av\s+Carlos\s+Graef\s+Fernández\s+No.*", 
        r"Tel.*", 
        r"Lic\. Sanitaria\s+\d{10}", 
        r"C\.P", 
        r"\b\d{5},?\b", 
        r"México\s+D\.F\.", 
        r"Cuarto:.*", 
        r"0001426761.*", 
        r"Fecha Impresión:.*", 
        r"NSO", 
        r"\d{1,4}-\d{1,4}", 
        r"Método.*", 
        r"Cédula Profesional.*" 
    ]
    
    cleaned_text = raw_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
    
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip() 

    return cleaned_text

# Función para enviar el texto filtrado a GPT y obtener la respuesta
def enviar_a_gpt(client, texto_limpio):
    if client is None:
        st.error("El cliente de OpenAI no está inicializado.")
        return None

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O el modelo que estés usando
            messages=[
                {"role": "system", "content": "Eres un útil asistente."},
                {"role": "user", "content": texto_limpio}
            ],
            max_tokens=500 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error al llamar a OpenAI: {e}")
        return None

def main():
    st.title("Aplicación Médica con Streamlit y OpenAI")
    
    openai_client = initialize_openai()

    if openai_client:
        st.write("Cliente de OpenAI inicializado correctamente.")
        
        archivos = st.file_uploader("Sube uno o más archivos PDF", type="pdf", accept_multiple_files=True)

        if archivos:
            st.write(f"Se han subido {len(archivos)} archivos.")

            for i, archivo in enumerate(archivos):
                text = extract_text(archivo)
                
                original_char_count = len(text)
                cleaned_text = clean_text(text)
                cleaned_char_count = len(cleaned_text)
                
                st.markdown(f"### Texto Original del Archivo {i+1}")
                st.text_area(f"Texto Original del Archivo {i+1}", value=text, height=300)
                st.write(f"Cantidad de caracteres originales: {original_char_count}")
                
                st.markdown(f"### Texto Limpio del Archivo {i+1}")
                st.text_area(f"Texto Limpio del Archivo {i+1}", value=cleaned_text, height=300)
                st.write(f"Cantidad de caracteres después de limpiar: {cleaned_char_count}")
                
                gpt_response = enviar_a_gpt(openai_client, cleaned_text)
                
                if gpt_response:
                    st.markdown(f"### Respuesta de GPT para el Archivo {i+1}")
                    st.text_area(f"Respuesta GPT del Archivo {i+1}", value=gpt_response, height=300)

            datos_paciente = formulario_datos()
            st.write("Datos del paciente recopilados.")
            st.write(datos_paciente)

            respuestas_interrogatorio = interrogatorio_gpt(datos_paciente, openai_client, modelo="gpt-3.5-turbo")
            
            if respuestas_interrogatorio:
                st.write("Respuestas al interrogatorio GPT recopiladas.")
                st.write(respuestas_interrogatorio)
        
        else:
            st.error("No se han subido archivos.") 
    else:
        st.error("No se pudo inicializar el cliente de OpenAI debido a problemas con la API Key.")

if __name__ == "__main__":
    main()
