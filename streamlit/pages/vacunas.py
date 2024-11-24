import streamlit as st
import requests
import os
from datetime import datetime

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def load_mascotas():
    """Cargar todas las mascotas desde la API."""
    try:
        response = requests.get(f"{API_URL}/mascotas/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar mascotas: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def load_veterinarios():
    """Cargar todos los veterinarios desde la API."""
    try:
        response = requests.get(f"{API_URL}/veterinarios/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al cargar veterinarios")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def registrar_vacuna(mascota_id, nombre_vacuna, fecha_aplicacion, fecha_proxima, veterinario_id, lote, notas):
    """Registrar una nueva vacuna."""
    try:
        response = requests.post(
            f"{API_URL}/mascotas/{mascota_id}/vacunas",
            json={
                "mascota_id": mascota_id,
                "nombre_vacuna": nombre_vacuna,
                "fecha_aplicacion": fecha_aplicacion,
                "fecha_proxima": fecha_proxima,
                "veterinario_id": veterinario_id,
                "lote": lote,
                "notas": notas
            }
        )
        if response.status_code == 201:
            st.success("Vacuna registrada exitosamente")
        else:
            st.error(f"Error al registrar la vacuna: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")

# Interfaz de usuario
st.title("Registrar Vacuna para Mascota")

# Cargar datos necesarios
mascotas = load_mascotas()
veterinarios = load_veterinarios()

if mascotas and veterinarios:
    with st.form("vacuna_form"):
        mascota_id = st.selectbox("Selecciona la Mascota", [m['id'] for m in mascotas])
        nombre_vacuna = st.text_input("Nombre de la Vacuna")
        fecha_aplicacion = st.date_input("Fecha de Aplicación", datetime.today())
        fecha_proxima = st.date_input("Fecha Próxima", datetime.today())
        veterinario_id = st.selectbox("Selecciona el Veterinario", [v['id'] for v in veterinarios])
        lote = st.text_input("Lote")
        notas = st.text_area("Notas (opcional)")

        submitted = st.form_submit_button("Registrar Vacuna")
        if submitted:
            if not nombre_vacuna or not lote:
                st.error("Por favor, completa todos los campos requeridos")
            else:
                registrar_vacuna(mascota_id, nombre_vacuna, fecha_aplicacion.isoformat(), fecha_proxima.isoformat(), veterinario_id, lote, notas)

else:
    st.info("No hay mascotas o veterinarios registrados en la base de datos.")