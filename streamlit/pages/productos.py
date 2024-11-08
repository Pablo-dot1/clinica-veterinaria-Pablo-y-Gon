import streamlit as st
import requests

API_URL_PRODUCTOS = "http://localhost:8000/productos/"

# Función para crear un nuevo producto
def crear_producto():
    st.header("Crear Producto")
    nombre = st.text_input("Nombre del Producto")
    categoria = st.selectbox("Categoría", ["Vitaminas", "Cremas Analgésicas", "Desparasitadores", "Productos de Belleza"])
    precio = st.number_input("Precio", min_value=0.0, step=0.1)
    stock = st.number_input("Stock", min_value=0, step=1)

    if st.button("Crear Producto"):
        data = {"nombre": nombre, "categoria": categoria, "precio": precio, "stock": stock}
        response = requests.post(API_URL_PRODUCTOS, json=data)
        if response.status_code == 201:
            st.success("Producto creado exitosamente")
        else:
            st.error("Error al crear el producto")

# Función para visualizar productos
def ver_productos():
    st.header("Inventario de Productos")
    response = requests.get(API_URL_PRODUCTOS)
    if response.status_code == 200:
        productos = response.json()
        for producto in productos:
            st.write(f"ID: {producto['id']} | Nombre: {producto['nombre']} | Categoría: {producto['categoria']} | Precio: {producto['precio']} | Stock: {producto['stock']}")
    else:
        st.error("No se pudieron cargar los productos")

# Función para actualizar stock de un producto
def actualizar_stock():
    st.header("Actualizar Stock")
    producto_id = st.number_input("ID del Producto", min_value=1)
    nuevo_stock = st.number_input("Nuevo Stock", min_value=0, step=1)

    if st.button("Actualizar Stock"):
        data = {"id": producto_id, "stock": nuevo_stock}
        response = requests.put(f"{API_URL_PRODUCTOS}/{producto_id}", json=data)
        if response.status_code == 200:
            st.success("Stock actualizado correctamente")
        else:
            st.error("Error al actualizar el stock")

# Función para registrar una venta
def registrar_venta():
    st.header("Registrar Venta de Producto")
    producto_id = st.number_input("ID del Producto", min_value=1)
    cantidad = st.number_input("Cantidad", min_value=1, step=1)

    if st.button("Registrar Venta"):
        data = {"producto_id": producto_id, "cantidad": cantidad}
        response = requests.post(f"{API_URL_PRODUCTOS}/venta", json=data)
        if response.status_code == 201:
            st.success("Venta registrada exitosamente")
        else:
            st.error("Error al registrar la venta")

# Llamar a las funciones según la opción seleccionada
opcion = st.selectbox("Selecciona una acción", ["Ver Inventario", "Crear Producto", "Actualizar Stock", "Registrar Venta"])

if opcion == "Crear Producto":
    crear_producto()
elif opcion == "Actualizar Stock":
    actualizar_stock()
elif opcion == "Registrar Venta":
    registrar_venta()
else:
    ver_productos()
