import streamlit as st
import requests
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def crear_veterinario(nombre, apellido, email, telefono, especialidad, numero_colegiado, horario_trabajo):
    """Registrar un nuevo veterinario."""
    try:
        response = requests.post(
            f"{API_URL}/veterinarios/",
            json={
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "telefono": telefono,
                "especialidad": especialidad,
                "numero_colegiado": numero_colegiado,
                "horario_trabajo": horario_trabajo
            }
        )
        if response.status_code == 201:
            st.success("Veterinario registrado exitosamente")
        else:
            st.error(f"Error al registrar el veterinario: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")

# Interfaz de usuario
st.title("Registrar Veterinario")

with st.form("veterinario_form"):
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")
    especialidad = st.text_input("Especialidad")
    numero_colegiado = st.text_input("Número Colegiado")
    horario_trabajo = st.text_input("Horario de Trabajo")

    submitted = st.form_submit_button("Registrar Veterinario")
    if submitted:
        if not nombre or not apellido or not email or not telefono or not especialidad or not numero_colegiado or not horario_trabajo:
            st.error("Por favor, completa todos los campos requeridos")
        else:
            crear_veterinario(nombre, apellido, email, telefono, especialidad, numero_colegiado, horario_trabajo)