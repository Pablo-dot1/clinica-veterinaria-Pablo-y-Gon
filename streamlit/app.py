import streamlit as st
import os
from PIL import Image  # Importar para cargar y manipular imágenes

# Configuración de la página
st.set_page_config(
    page_title="Clínica Veterinaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar la estética
st.markdown("""
    <style>
    .main {
        padding: 2rem 2.5rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.7rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .reportview-container {
        background: linear-gradient(to bottom right, #ffffff, #f0f2f6);
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
    }
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    /* Estilo para los cuadros de texto */
    .welcome-box {
        background-color: #e9ecef;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h2 {
        color: #34495e;
        font-size: 2rem;
    }
    p {
        color: #7f8c8d;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    /* Título de la página */
    .page-title {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación con mejor formato
st.markdown("""
    <div class='page-title'>
        <h1 style='text-align: center; color: #34495e;'>Clínica Veterinaria Pablo y Gonzalo</h1>
    </div>
""", unsafe_allow_html=True)

# Ruta de la imagen (dentro de la carpeta del proyecto)
image_path = "imagenes/imagen1.jpg"

# Mostrar la imagen en la aplicación
st.image(image_path, caption="Clínica Veterinaria", width=1100)  # Ancho ajustado a 1100 píxeles para mejor visualización

# Mensaje de bienvenida orientado al dueño de la clínica
st.markdown("""
    <div class='welcome-box'>
        <h2 style='text-align: center;'>¡Bienvenido a la gestión de la Clínica Veterinaria!</h2>
        <p style='text-align: center;'>
            Como dueño de la clínica, tienes acceso a las siguientes funciones para facilitar la administración:
            <ul style='text-align: left;'>
                <li>Registrar y gestionar citas para consultas veterinarias</li>
                <li>Administrar el registro de clientes y sus mascotas</li>
                <li>Controlar el inventario de productos</li>
                <li>Gestionar los tratamientos disponibles</li>
                <li>Visualización de gráficos en Dashboard</li>
            </ul>
            Para cualquier consulta no dudes en escribirnos.
        </p>
    </div>
""", unsafe_allow_html=True)
