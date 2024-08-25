import streamlit as st
from pdfminer.high_level import extract_text
import re

# Función para limpiar el texto extraído
def clean_text(raw_text):
    # Expresiones regulares para identificar y eliminar información repetitiva y no relevante
    patterns_to_remove = [
        r"Campus Santa Fe[\s\S]*?México D.F.Tel. 1103-1600 Lic. Sanitaria 1005001030",
        r"PACIENTE:.*",
        r"(ILLESCAS RAMOS RUBEN \d{10} Cuarto:)",
        r"Fecha Nac:.*",
        r"Género: [MF] Edad: \d+ Años",
        r"No\. Orden \d+",
        r"Servicio:.*",
        r"Fecha Solicitud:.*",
        r"Fecha Toma:.*",
        r"Fecha Impresión:.*",
        r"Usuario:.*",
        r"Instrumento:.*",
        r"Metodo:.*",
        r"Campus: Santa Fe",
        r"NOTA:.*",
        r"Relación [\s\S]*?Usuario:.*",
        r"Examen General de Orina [\s\S]*?Usuario:.*",
        r"SANGRE OCULTA EN HECES [\s\S]*?Usuario:.*",
        r"Grupo sanguíneo y RH [\s\S]*?Usuario:.*",
        r"^\d+ de \d+",
        r"Dr\. \w+ \w+ \w+ Cedula Profesional \d+"
    ]
    
    cleaned_text = raw_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text)

    # Eliminar líneas en blanco y espacios adicionales
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

# Función para extraer los valores de los estudios médicos
def extract_medical_values(text):
    # Definir patrones para extraer valores y unidades
    # Ejemplo: Hemoglobina 16.0 g/dL, Eritrocitos 5.32 10^6/uL
    pattern = re.compile(
        r"(Leucocitos|Eritrocitos|Hemoglobina|Hematocrito|Volumen corpuscular medio|Concentración media de hemoglobina|"
        r"Concentración media de hemoglobina corpuscular|Ancho de distribución RDW-CV|Plaquetas|Volumen medio plaquetario|"
        r"Neutrofilos porcentaje|Linfocitos porcentaje|Monocitos porcentaje|Eosinofilos porcentaje|Basofilos porcentaje|"
        r"Neutrofilos absolutos|Linfocitos absolutos|Monocitos absolutos|Eosinofilos absolutos|Basofilos absolutos|"
        r"Velocidad de sedimentacion globular|Hemoglobina Glucosilada A1c|Glucosa en suero|Nitrogeno ureico en Suero|"
        r"Creatinina en Suero|Cistatina C|Tasa de filtracion glomerular|Urato en Suero|Calcio en Suero|Fosfato en Suero|"
        r"Colesterol Total en suero|Trigliceridos en Suero|Colesterol HDL|Colesterol LDL|Colesterol de muy baja densidad VLDL|"
        r"Colesterol Total/ Colesterol HDL|Colesterol LDL / HDL|Apolipoproteína B en suero|Aspartato Aminotransferasa en suero|"
        r"Alanino Aminotransferasa en suero|Fosfatasa Alcalina en Suero|LDH Deshidrogenasa Láctica|Gamma Glutamil Transferasa|"
        r"Bilirrubina total en Suero|Bilirrubina directa en Suero|Bilirrubina indirecta en Suero|Proteínas totales|Albumina en Suero|"
        r"Globulina en suero|Relación A/G en suero|Proteína C Reactiva ultrasensible|Homocisteina en Suero|TSH Tirotropina Ultrasensible en suero|"
        r"Antigeno Prostatico Específico|VIH 1/2 Ac \+ Ag p24 en Suero|Examen General de Orina Color|Aspecto|Gravedad específica|pH|"
        r"Nitritos|Esterasa leucocitaria|Proteínas|Glucosa|Cetonas|Urobilinógeno|Bilirrubinas|Hemoglobina|Leucocitos|Eritrocitos|"
        r"Células Epiteliales|Bacterias|Gram|Cristales|Levaduras|Filamento mucoide|SANGRE OCULTA EN HECES|Coproparasitoscopico|"
        r"Grupo sanguíneo y RH)\s*:\s*([0-9\.]+)\s*([a-zA-Z0-9^/%µ]*\s*/[a-zA-Z0-9^%µ]*.*?)(?=Campus|\Z)",
        re.IGNORECASE
    )

    matches = pattern.findall(text)
    extracted_values = [{"estudio": match[0], "valor": match[1], "unidad": match[2]} for match in matches]

    return extracted_values

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
        
        # Extraer valores médicos del texto limpio
        extracted_values = extract_medical_values(cleaned_text)
        
        # Mostrar el texto original, el texto limpio y los valores extraídos, junto con las cantidades de caracteres
        st.markdown(f"### Texto Original del Archivo {i+1}")
        st.text_area(f"Texto Original del Archivo {i+1}", value=text, height=300)
        st.write(f"Cantidad de caracteres originales: {original_char_count}")
        
        st.markdown(f"### Texto Limpio del Archivo {i+1}")
        st.text_area(f"Texto Limpio del Archivo {i+1}", value=cleaned_text, height=300)
        st.write(f"Cantidad de caracteres después de limpiar: {cleaned_char_count}")
        
        st.markdown(f"### Valores Extraídos del Archivo {i+1}")
        for val in extracted_values:
            st.write(f"Estudio: {val['estudio']}, Valor: {val['valor']}, Unidad: {val['unidad']}")
