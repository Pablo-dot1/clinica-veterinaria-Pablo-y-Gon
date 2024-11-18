import streamlit as st
import requests
import json
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def load_clientes():
    try:
        response = requests.get(f"{API_URL}/clientes/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar clientes: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def update_cliente(cliente_id, nombre, email, telefono):
    try:
        response = requests.put(
            f"{API_URL}/clientes/{cliente_id}",
            json={
                "nombre": nombre,
                "email": email,
                "telefono": telefono
            }
        )
        if response.status_code == 200:
            st.success("Cliente actualizado exitosamente")
            return True
        else:
            st.error("Error al actualizar el cliente")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

def delete_cliente(cliente_id):
    try:
        response = requests.delete(f"{API_URL}/clientes/{cliente_id}")
        if response.status_code == 200:
            st.success("Cliente eliminado exitosamente")
            return True
        else:
            st.error("Error al eliminar el cliente")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

st.title("Gestión de Clientes")

# Tabs para diferentes operaciones
tab1, tab2, tab3, tab4 = st.tabs(["Ver Clientes", "Agregar Cliente", "Actualizar Cliente", "Eliminar Cliente"])

with tab1:
    # Cargar y mostrar clientes
    clientes = load_clientes()

    if clientes:
        st.write("### Lista de Clientes")
        cliente_data = []
        for cliente in clientes:
            cliente_data.append({
                "ID": cliente.get("id", "N/A"),
                "Nombre": cliente.get("nombre", "N/A"),
                "Email": cliente.get("email", "N/A"),
                "Teléfono": cliente.get("telefono", "N/A")
            })
        
        st.table(cliente_data)
    else:
        st.info("No hay clientes registrados")

with tab2:
    # Formulario para agregar nuevo cliente
    st.write("### Agregar Nuevo Cliente")
    with st.form("nuevo_cliente_form"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        
        submitted = st.form_submit_button("Agregar Cliente")
        if submitted:
            if not nombre or not email or not telefono:
                st.error("Por favor, complete todos los campos")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/clientes/",
                        json={
                            "nombre": nombre,
                            "email": email,
                            "telefono": telefono
                        }
                    )
                    if response.status_code == 201:
                        st.success("Cliente agregado exitosamente")
                        st.experimental_rerun()
                    else:
                        st.error("Error al agregar el cliente")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")

with tab3:
    # Formulario para actualizar cliente
    st.write("### Actualizar Cliente")
    with st.form("actualizar_cliente_form"):
        cliente_id = st.number_input("ID del Cliente", min_value=1, step=1)
        nombre = st.text_input("Nuevo Nombre")
        email = st.text_input("Nuevo Email")
        telefono = st.text_input("Nuevo Teléfono")
        
        submitted = st.form_submit_button("Actualizar Cliente")
        if submitted:
            if not nombre or not email or not telefono:
                st.error("Por favor, complete todos los campos")
            else:
                if update_cliente(cliente_id, nombre, email, telefono):
                    st.experimental_rerun()

with tab4:
    # Formulario para eliminar cliente
    st.write("### Eliminar Cliente")
    cliente_id = st.number_input("ID del Cliente a Eliminar", min_value=1, step=1)
    if st.button("Eliminar Cliente"):
        if delete_cliente(cliente_id):
            st.experimental_rerun()
