# funciones/recepcion_docs.py
import streamlit as st

def cargar_documentos():
    st.header("Carga de Documentos PDF")
    archivos = st.file_uploader("Sube archivos PDF", type="pdf", accept_multiple_files=True, key="file_uploader")
    
    if archivos:
        # Mostrar detalles de los archivos subidos (opcional)
        for archivo in archivos:
            st.write(f"Archivo subido: {archivo.name} ({archivo.size//1024} KB)")
        
        return archivos
    return None
