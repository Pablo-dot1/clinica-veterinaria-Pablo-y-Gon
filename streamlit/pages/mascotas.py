import streamlit as st
import requests
import json
import os
from urllib.parse import parse_qs

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def load_mascotas():
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

def get_cliente(cliente_id):
    try:
        response = requests.get(f"{API_URL}/clientes/{cliente_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

st.title("Gestión de Mascotas")

# Obtener cliente_id de los parámetros de URL o input
params = st.query_params
cliente_id = params.get('cliente_id', [None])[0]

if not cliente_id:
    cliente_id = st.number_input("ID del Cliente", min_value=1, step=1)

if cliente_id:
    cliente = get_cliente(cliente_id)
    if cliente:
        st.success(f"Registrando mascota para el cliente: {cliente['nombre']} {cliente['apellido']}")
        
        # Tabs para diferentes operaciones
        tab1, tab2, tab3, tab4 = st.tabs(["Ver Mascotas", "Agregar Mascota", "Actualizar Mascota", "Eliminar Mascota"])

        with tab1:
            # Cargar y mostrar mascotas del cliente
            try:
                response = requests.get(f"{API_URL}/mascotas/cliente/{cliente_id}")
                if response.status_code == 200:
                    mascotas = response.json()
                    if mascotas:
                        st.write("### Mascotas del Cliente")
                        mascota_data = []
                        for mascota in mascotas:
                            mascota_data.append({
                                "ID": mascota.get("id", "N/A"),
                                "Nombre": mascota.get("nombre", "N/A"),
                                "Especie": mascota.get("especie", "N/A"),
                                "Raza": mascota.get("raza", "N/A"),
                                "Edad": mascota.get("edad", "N/A"),
                                "Peso": mascota.get("peso", "N/A")
                            })
                        st.table(mascota_data)
                    else:
                        st.info("Este cliente no tiene mascotas registradas")
            except requests.exceptions.RequestException as e:
                st.error(f"Error al cargar las mascotas: {str(e)}")

        with tab2:
            # Formulario para agregar nueva mascota
            st.write("### Agregar Nueva Mascota")
            with st.form("nueva_mascota_form"):
                nombre = st.text_input("Nombre")
                especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
                raza = st.text_input("Raza")
                fecha_nacimiento = st.date_input("Fecha de nacimiento")
                edad = st.number_input("Edad (años)", min_value=0, value=0)
                peso = st.number_input("Peso (kg)", min_value=0.1, max_value=200.0, value=1.0, step=0.1)
                sexo = st.selectbox("Sexo", ["M", "H"])
                alergias = st.text_area("Alergias (opcional)")
                condiciones_especiales = st.text_area("Condiciones especiales (opcional)")
                
                submitted = st.form_submit_button("Agregar Mascota")
                if submitted:
                    if not nombre or not especie or not raza:
                        st.error("Por favor, complete todos los campos")
                    else:
                        try:
                            response = requests.post(
                                f"{API_URL}/mascotas/",
                                json={
                                    "nombre": nombre,
                                    "especie": especie,
                                    "raza": raza,
                                    "edad": edad,
                                    "peso": peso,
                                    "cliente_id": cliente_id,
                                    "fecha_nacimiento": fecha_nacimiento.isoformat(),
                                    "sexo": sexo,
                                    "alergias": alergias if alergias.strip() else None,
                                    "condiciones_especiales": condiciones_especiales if condiciones_especiales.strip() else None
                                }
                            )
                            if response.status_code == 201:
                                st.success("Mascota agregada exitosamente")
                                st.rerun()
                            else:
                                st.error(f"Error al agregar la mascota: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error de conexión: {str(e)}")

        with tab3:
            # Formulario para actualizar mascota
            st.write("### Actualizar Mascota")
            with st.form("actualizar_mascota_form"):
                mascota_id = st.number_input("ID de la Mascota", min_value=1, step=1)
                nombre = st.text_input("Nuevo Nombre")
                especie = st.text_input("Nueva Especie")
                raza = st.text_input("Nueva Raza")
                edad = st.number_input("Nueva Edad (años)", min_value=0, value=0)
                peso = st.number_input("Nuevo Peso (kg)", min_value=0.0, value=0.0)
                
                submitted = st.form_submit_button("Actualizar Mascota")
                if submitted:
                    if not nombre or not especie or not raza:
                        st.error("Por favor, complete todos los campos")
                    else:
                        try:
                            response = requests.put(
                                f"{API_URL}/mascotas/{mascota_id}",
                                json={
                                    "nombre": nombre,
                                    "especie": especie,
                                    "raza": raza,
                                    "edad": edad,
                                    "peso": peso,
                                    "cliente_id": cliente_id
                                }
                            )
                            if response.status_code == 200:
                                st.success("Mascota actualizada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al actualizar la mascota")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error de conexión: {str(e)}")

        with tab4:
            # Formulario para eliminar mascota
            st.write("### Eliminar Mascota")
            mascota_id = st.number_input("ID de la Mascota a Eliminar", min_value=1, step=1)
            if st.button("Eliminar Mascota"):
                try:
                    response = requests.delete(f"{API_URL}/mascotas/{mascota_id}")
                    if response.status_code in [200, 204]:
                        st.success("Mascota eliminada exitosamente")
                        st.rerun()
                    else:
                        st.error(f"Error al eliminar la mascota: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")
    else:
        st.error("Cliente no encontrado")
else:
    st.info("Por favor, ingrese el ID del cliente para gestionar sus mascotas")