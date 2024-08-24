# app.py
import streamlit as st
from gpt_config.openai_setup import initialize_openai
from file_utils.pdf_utils import extract_text_from_pdf
from file_utils.text_processing import clean_and_structure_text, calculate_bmi
import json

# Inicializar OpenAI
openai = initialize_openai()

# Leer el contenido del archivo de prompt
with open("gpt_config/prompt.txt", "r") as f:
    prompt_template = f.read()

st.title("Análisis de Resultados Médicos con IA")

# Subida de PDF
st.header("Sube tus estudios médicos en PDF")
uploaded_files = st.file_uploader("Elige archivos PDF", type="pdf", accept_multiple_files=True)

# Ingreso de datos adicionales
st.header("Datos del Paciente")
age = st.number_input("Edad", min_value=0)
weight = st.number_input("Peso (kg)", min_value=0)
height = st.number_input("Altura (m)", min_value=0.5, max_value=2.5)
gender = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
conditions = st.text_area("Enfermedades conocidas")
medications = st.text_area("Medicamentos actuales")
symptoms = st.text_area("Síntomas")

user_data = {
    "age": age,
    "weight": weight,
    "height": height,
    "bmi": calculate_bmi(weight, height),
    "gender": gender,
    "conditions": conditions,
    "medications": medications,
    "symptoms": symptoms
}

# Verificación si se han subido archivos
if uploaded_files:
    all_texts = []
    for uploaded_file in uploaded_files:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area(f"Texto extraído del PDF {uploaded_file.name}", text, height=200)
        clean_text = clean_and_structure_text(text)
        all_texts.append(clean_text)
    
    # Generar un prompt combinando todos los textos y datos del usuario
    combined_texts = {
        "historical_tests": all_texts[:-1],
        "current_tests": all_texts[-1],
        "patient": user_data
    }

    # Reemplazar los marcadores de posición en el prompt
    prompt = prompt_template.format(
        age=user_data["age"],
        weight=user_data["weight"],
        height=user_data["height"],
        bmi=user_data["bmi"],
        gender=user_data["gender"],
        conditions=user_data["conditions"],
        medications=user_data["medications"],
        symptoms=user_data["symptoms"],
        medical_report_data=json.dumps(combined_texts, indent=2)
    )

    # Botón para iniciar el análisis de IA
    if st.button("Obtener Análisis"):
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=prompt,
            max_tokens=1500
        )
        analysis_text = response.choices[0].text
        st.subheader("Análisis de IA:")
        st.write(analysis_text)

# Aquí añadiremos más funcionalidades en los siguientes pasos
