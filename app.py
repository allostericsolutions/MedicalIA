import streamlit as st
from pdfminer.high_level import extract_text
import re

# Función para limpiar el texto extraído
def clean_text(raw_text):
    # Expresiones regulares para identificar y eliminar información repetitiva
    patterns_to_remove = [
        r"Campus Santa Fe[\s\S]*?México D.F.Tel. 1103-1600 Lic. Sanitaria 1005001030",
        r"PACIENTE:.*",
        r"Médico:.*",
        r"Fecha Solicitud:.*",
        r"Fecha Toma:.*",
        r"Fecha Impresión:.*",
        r"Usuario:.*",
        r"Instrumento:.*",
        r"Metodo:.*"
    ]
    
    cleaned_text = raw_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Eliminar líneas en blanco y espacios adicionales
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

# Subida de Archivos
uploaded_files = st.file_uploader("Sube uno o más archivos PDF", type="pdf", accept_multiple_files=True)

# Verificar si se han subido archivos
if uploaded_files:
    st.write(f"Se han subido {len(uploaded_files)} archivos.")
    
    for i, uploaded_file in enumerate(uploaded_files):
        # Extraer el texto usando pdfminer
        text = extract_text(uploaded_file)
        
        # Limpiar el texto
        cleaned_text = clean_text(text)
        
        # Mostrar el texto original y el texto limpio
        st.markdown(f"### Texto Original del Archivo {i+1}")
        st.text_area(f"Texto Original del Archivo {i+1}", value=text, height=300)
        
        st.markdown(f"### Texto Limpio del Archivo {i+1}")
        st.text_area(f"Texto Limpio del Archivo {i+1}", value=cleaned_text, height=300)
