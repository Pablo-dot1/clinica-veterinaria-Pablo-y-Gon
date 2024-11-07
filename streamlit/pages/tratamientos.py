import streamlit as st
import requests

API_URL_TRATAMIENTOS = "http://localhost:8000/tratamientos/"

# Función para crear un nuevo tratamiento
def crear_tratamiento():
    st.header("Crear Tratamiento")
    nombre = st.text_input("Nombre del Tratamiento")
    descripcion = st.text_area("Descripción del Tratamiento")
    costo = st.number_input("Costo", min_value=0.0, step=0.1)

    if st.button("Crear Tratamiento"):
        data = {"nombre": nombre, "descripcion": descripcion, "costo": costo}
        response = requests.post(API_URL_TRATAMIENTOS, json=data)
        if response.status_code == 201:
            st.success("Tratamiento creado exitosamente")
        else:
            st.error("Error al crear el tratamiento")

# Función para visualizar los tratamientos
def ver_tratamientos():
    st.header("Tratamientos Disponibles")
    response = requests.get(API_URL_TRATAMIENTOS)
    if response.status_code == 200:
        tratamientos = response.json()
        for tratamiento in tratamientos:
            st.write(f"ID: {tratamiento['id']} | Nombre: {tratamiento['nombre']} | Costo: {tratamiento['costo']}")
    else:
        st.error("No se pudieron cargar los tratamientos")

# Función para modificar un tratamiento
def modificar_tratamiento():
    st.header("Modificar Tratamiento")
    tratamiento_id = st.number_input("ID del Tratamiento", min_value=1)
    nombre = st.text_input("Nuevo Nombre del Tratamiento")
    descripcion = st.text_area("Nueva Descripción")
    costo = st.number_input("Nuevo Costo", min_value=0.0, step=0.1)

    if st.button("Modificar Tratamiento"):
        data = {"nombre": nombre, "descripcion": descripcion, "costo": costo}
        response = requests.put(f"{API_URL_TRATAMIENTOS}/{tratamiento_id}", json=data)
        if response.status_code == 200:
            st.success("Tratamiento modificado correctamente")
        else:
            st.error("Error al modificar el tratamiento")

# Función para eliminar un tratamiento
def eliminar_tratamiento():
    st.header("Eliminar Tratamiento")
    tratamiento_id = st.number_input("ID del Tratamiento", min_value=1)

    if st.button("Eliminar Tratamiento"):
        response = requests.delete(f"{API_URL_TRATAMIENTOS}/{tratamiento_id}")
        if response.status_code == 200:
            st.success("Tratamiento eliminado correctamente")
        else:
            st.error("Error al eliminar el tratamiento")

# Llamar a las funciones según la opción seleccionada
opcion = st.selectbox("Selecciona una acción", ["Ver Tratamientos", "Crear Tratamiento", "Modificar Tratamiento", "Eliminar Tratamiento"])

if opcion == "Crear Tratamiento":
    crear_tratamiento()
elif opcion == "Modificar Tratamiento":
    modificar_tratamiento()
elif opcion == "Eliminar Tratamiento":
    eliminar_tratamiento()
else:
    ver_tratamientos()
