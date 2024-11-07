import streamlit as st
import requests
from datetime import datetime

API_URL_CITAS = "http://localhost:8000/citas/"

def crear_cita():
    st.header("Crear Cita")
    mascota_id = st.number_input("ID de la Mascota", min_value=1)
    fecha_hora = st.datetime_input("Fecha y Hora de la Cita")
    motivo = st.text_input("Motivo de la Cita")

    if st.button("Crear Cita"):
        data = {"mascota_id": mascota_id, "fecha_hora": fecha_hora, "motivo": motivo}
        response = requests.post(API_URL_CITAS, json=data)
        if response.status_code == 201:
            st.success("Cita creada exitosamente")
        else:
            st.error("Error al crear la cita")

def ver_citas():
    st.header("Citas")
    response = requests.get(API_URL_CITAS)
    if response.status_code == 200:
        citas = response.json()
        for cita in citas:
            st.write(f"ID: {cita['id']} | Fecha: {cita['fecha_hora']} | Motivo: {cita['motivo']}")
    else:
        st.error("No se pudieron cargar las citas")

# Llamar a las funciones según la opción seleccionada
opcion = st.selectbox("Selecciona una acción", ["Ver Citas", "Crear Cita"])

if opcion == "Crear Cita":
    crear_cita()
else:
    ver_citas()
