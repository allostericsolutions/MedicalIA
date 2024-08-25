import streamlit as st
from pdfminer.high_level import extract_text
import re

# Función para limpiar el texto extraído
def clean_text(raw_text):
    # Expresiones regulares para identificar y eliminar encabezados, notas y detalles no relevantes
    patterns_to_remove = [
        r"PACIENTE:.*",                        # Encabezado de paciente
        r"\d+ de \d+",                         # Números de página (1 de 7, etc.)
        r"Fecha [A-Za-z]+:.*",                 # Encabezado de Fecha (Solicitud, Toma, Impresión)
        r"Género: \w+",                        # Encabezado de género
        r"Edad: \d+ Años",                     # Encabezado de edad
        r"No\. Orden .*",                      # Encabezado de número de orden
        r"Médico:.*",                          # Encabezado de médico
        r"Servicio:.*",                        # Encabezado de servicio
        r"Campus:.*",                          # Información sobre el campus
        r"Instrumento:.*",                     # Instrumento utilizado
        r"Usuario:.*",                         # Usuario que hizo el análisis
        r"Metodo:.*",                          # Método utilizado
        r"NOTA:.*",                            # Notas
        r"Jefe de laboratorio.*",              # Jefe de laboratorio
        r"JEFE LABORATORIO.*",                 # Jefe de laboratorio en mayúsculas
        r"Sucursal.*",                         # Sucursal
        r"Liberó.*",                           # Liberó
        r"Paciente.*",                         # Paciente
        r"N° Paciente.*",                      # Número de Paciente
        r"interpretación deberá.*",            # Frases de interpretación
        r"Página.*",                           # Página
        r"\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+.*",  # Nombre del paciente repetido
        r"\b[0-3]?\d/[0-1]?\d/\d{4}\b",        # Fechas (formato día/mes/año)
        r"\b[0-2]?\d:[0-5]?\d:[0-5]?\d\b",     # Fechas (formato hora:minuto:segundo)
        r"Av\s+Carlos\s+Graef\s+Fernández\s+No.*",  # Dirección repetitiva
        r"Tel.*",                              # Teléfonos
        r"Lic\. Sanitaria\s+\d{10}",           # Licencias Sanitarias
        r"\bC\.P\.\s\d{5}\b",                  # Código Postal cualquier C.P 5 cifras
        r"México\s+D\.F\.",                    # Ubicación, México D.F
        r"Cuarto:.*",                          # Información de cuarto específico
        r"0001426761.*",                       # Información específica del paciente
        r"Fecha Impresión:.*",                 # Fechas de impresión
        r"NSO",                                # Información de NSO
        r"\d{1,4}-\d{1,4}",                    # Rangos numéricos como 70-1190, 0.00-150.00, 150-500
        r"Método.*",                           # Método
        r"Cédula Profesional.*"                # Cédula Profesional
    ]
    
    cleaned_text = raw_text
    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)

    # Retirar líneas vacías y espacios adicionales
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)  # Retirar múltiples saltos de línea
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Retirar espacios adicionales

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
