
import streamlit as st
from pdfminer.high_level import extract_text
import re

# Función para extraer líneas que contienen estudios y sus valores
def extract_medical_values(text):
    # Expresión regular para encontrar líneas con valores numéricos
    pattern = re.compile(r"(.+?):?\s+([0-9.]+)\s*([a-zA-Z/\^%µ]*\s*/?[a-zA-Z0-9^%µ]*)")
    
    matches = pattern.findall(text)
    extracted_values = [{"estudio": match[0].strip(), "valor": match[1], "unidad": match[2].strip()} for match in matches]

    # Filtrar valores irrelevantes
    filtered_values = [val for val in extracted_values if not re.match(r"^\d+ de \d+|^Fecha|^Médico|^Paciente|^Servicio|^NOTA|^Usuario|^Instrumento|^Metodo|^Campus|^Gravedad específica|^pH|^Nitritos|^Esterasa leucocitaria|^Proteínas|^Glucosa|^Cetonas|^Urobilinógeno|^Bilirrubinas|^Hemoglobina|^Leucocitos|^Eritrocitos|^Células Epiteliales|^Bacterias|^Gram|^Cristales|^Levaduras|^Filamento mucoide|^SANGRE OCULTA EN HECES|^Coproparasitoscopico|^Grupo sanguíneo y RH", val['estudio'], re.IGNORECASE)]
    
    return filtered_values

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
        
        # Procesar el texto para extraer valores médicos
        extracted_values = extract_medical_values(text)
        
        # Filtrar texto limpio basado en los valores extraídos
        cleaned_text = '\n'.join([f"{val['estudio']}: {val['valor']} {val['unidad']}" for val in extracted_values])
        
        # Contar caracteres después de la limpieza
        cleaned_char_count = len(cleaned_text)
        
        # Mostrar el texto original, el texto limpio y los valores extraídos, junto con las cantidades de caracteres
        st.markdown(f"### Texto Original del Archivo {i+1}")
        st.text_area(f"Texto Original del Archivo {i+1}", value=text, height=300)
        st.write(f"Cantidad de caracteres originales: {original_char_count}")
        
        st.markdown(f"### Texto Limpio del Archivo {i+1}")
        st.text_area(f"Texto Limpio del Archivo {i+1}", value=cleaned_text, height=300)
        st.write(f"Cantidad de caracteres después de limpiar: {cleaned_char_count}")
        
        st.markdown(f"### Valores Extraídos del Archivo {i+1}")
        for val in extracted_values:
            st.write(f"**Estudio:** {val['estudio']} **Valor:** {val['valor']} **Unidad:** {val['unidad']}")
