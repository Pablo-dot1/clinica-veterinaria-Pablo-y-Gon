import streamlit as st
import requests
import pandas as pd
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://fastapi:8000')

# Función para crear un nuevo producto
def crear_producto():
    st.header("Crear Producto")
    nombre = st.text_input("Nombre del Producto")
    descripcion = st.text_area("Descripción del Producto")
    categoria = st.selectbox("Categoría", ["Vitaminas", "Cremas Analgésicas", "Desparasitadores", "Productos de Belleza"])
    precio = st.number_input("Precio", min_value=0.0, step=0.1)
    stock = st.number_input("Stock", min_value=0, step=1)
    proveedor = st.text_input("Proveedor")  # Agregar el campo proveedor

    if st.button("Crear Producto"):
        datos = {
            "nombre": nombre,
            "descripcion": descripcion,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "proveedor": proveedor  # Asegúrate de incluir el proveedor en los datos
        }
        respuesta = requests.post(f"{API_URL}/productos/", json=datos)
        if respuesta.status_code == 201:
            st.success("Producto creado exitosamente")
        else:
            st.error("Error al crear el producto")

# Función para actualizar stock de un producto
def actualizar_stock():
    st.header("Actualizar Stock")
    id_producto = st.number_input("ID del Producto", min_value=1)
    nuevo_stock = st.number_input("Nuevo Stock", min_value=0, step=1)

    if st.button("Actualizar Stock"):
        if nuevo_stock is None or nuevo_stock < 0:
            st.error("El stock debe ser un número no negativo.")
        else:
            # Construir la URL con el stock como parámetro de consulta
            url = f"{API_URL}/productos/{id_producto}?stock={nuevo_stock}"
            respuesta = requests.put(url)
            if respuesta.status_code == 200:
                st.success("Stock actualizado correctamente")
            else:
                st.error(f"Error al actualizar el stock: {respuesta.status_code} - {respuesta.text}")
# Función para eliminar un producto
def eliminar_producto():
    st.header("Eliminar Producto")
    id_producto = st.number_input("ID del Producto a Eliminar", min_value=1)

    if st.button("Eliminar Producto"):
        respuesta = requests.delete(f"{API_URL}/productos/{id_producto}")
        if respuesta.status_code == 204:
            st.success("Producto eliminado exitosamente")
        else:
            st.error("Error al eliminar el producto")

# Función para visualizar productos
def ver_productos():
    st.header("Inventario de Productos")
    respuesta = requests.get(f"{API_URL}/productos/")
    if respuesta.status_code == 200:
        productos = respuesta.json()
        
        # Crear un DataFrame de pandas para facilitar la visualización
        df_productos = pd.DataFrame(productos)
        
        # Mostrar el DataFrame como una tabla
        st.dataframe(df_productos)  # Esto mostrará los productos en una tabla interactiva
        
    else:
        st.error("No se pudieron cargar los productos")

# Crear pestañas para diferentes acciones
st.title("Gestión de Productos")
tab1, tab2, tab3, tab4 = st.tabs(["Crear Producto", "Actualizar Stock", "Eliminar Producto", "Ver Inventario"])

with tab1:
    crear_producto()

with tab2:
    actualizar_stock()

with tab3:
    eliminar_producto()

with tab4:
    ver_productos()