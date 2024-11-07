import streamlit as st
import requests

API_URL = "http://localhost:8000/clientes/"  # Asegúrate de que el backend esté corriendo

# Función para crear un nuevo cliente
def crear_cliente():
    st.header("Crear Cliente")
    nombre = st.text_input("Nombre")
    telefono = st.text_input("Teléfono")
    direccion = st.text_input("Dirección")

    if st.button("Crear Cliente"):
        data = {"nombre": nombre, "telefono": telefono, "direccion": direccion}
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            st.success("Cliente creado exitosamente")
        else:
            st.error("Error al crear el cliente")

# Función para visualizar clientes
def ver_clientes():
    st.header("Clientes")
    response = requests.get(API_URL)
    if response.status_code == 200:
        clientes = response.json()
        for cliente in clientes:
            st.write(f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | Teléfono: {cliente['telefono']}")
    else:
        st.error("No se pudieron cargar los clientes")

# Llamar a las funciones según la opción seleccionada
opcion = st.selectbox("Selecciona una acción", ["Ver Clientes", "Crear Cliente"])

if opcion == "Crear Cliente":
    crear_cliente()
else:
    ver_clientes()
