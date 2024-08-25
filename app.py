import streamlit as st
from pdfminer.high_level import extract_text
import re

# Función para limpiar el texto extraído
def clean_text(raw_text):
    # Expresiones regulares para identificar y eliminar encabezados, notas y detalles no relevantes
    patterns_to_remove = [
        r"PACIENTE:.*",           # Encabezado de paciente
        r"\d+ de \d+",            # Números de página
        r"Fecha Nac:.*",          # Encabezado de fecha de nacimiento
        r"Género: .* Edad: .*",   # Encabezado de género y edad
        r"No. Orden .*",          # Encabezado de número de orden
        r"Fecha Solicitud:.*",    # Encabezado de fecha de solicitud
        r"Fecha Toma:.*",         # Encabezado de fecha de toma
        r"Fecha Impresión:.*",    # Encabezado de fecha de impresión
        r"Médico:.*",             # Encabezado de médico
        r"Servicio:.*",           # Encabezado de servicio
        r"Campus:.*",             # Encabezado de campus
        r"Instrumento:.*",        # Encabezado de instrumento
        r"Usuario:.*",            # Encabezado de usuario
        r"Metodo:.*",             # Encabezado de método
        r"NOTA:.*",               # Notas
        r"\b\w{,3}\b"             # Palabras pequeñas
    ]
    
    cleaned_text = raw_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Eliminar espacios adicionales y líneas en blanco
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
        
        # Contar caracteres antes de la limpieza
        original_char_count = len(text)
        
        # Limpiar el texto
        cleaned_text = clean_text(text)
        
        # Contar caracteres después de la limpieza
        cleaned_char_count = len(cleaned_text)
        
        # Mostrar el texto original y el texto limpio junto con las cantidades de caracteres
        st.markdown(f"### Texto Original del Archivo {i+1}")
        st.text_area(f"Texto Original del Archivo {i+1}", value=text, height=300)
        st.write(f"Cantidad de caracteres originales: {original_char_count}")
        
        st.markdown(f"### Texto Limpio del Archivo {i+1}")
        st.text_area(f"Texto Limpio del Archivo {i+1}", value=cleaned_text, height=300)
        st.write(f"Cantidad de caracteres después de limpiar: {cleaned_char_count}")
