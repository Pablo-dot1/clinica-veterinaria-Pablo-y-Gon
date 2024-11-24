import streamlit as st
import requests
from datetime import date
import os
import pandas as pd

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def get_mascotas_by_cliente(cliente_id):
    """Obtener todas las mascotas de un cliente"""
    try:
        response = requests.get(f"{API_URL}/mascotas/cliente/{cliente_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener mascotas: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def get_mascota_details(mascota_id):
    """Obtener detalles de una mascota específica"""
    try:
        response = requests.get(f"{API_URL}/mascotas/{mascota_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("No se pudo obtener la información de la mascota")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

def registrar_mascota(cliente_id, nombre, especie, raza, fecha_nacimiento, edad, peso, sexo, alergias="", condiciones_especiales=""):
    """Registrar una nueva mascota"""
    try:
        # Convertir fecha_nacimiento a string en formato ISO
        fecha_nacimiento_str = fecha_nacimiento.isoformat() if fecha_nacimiento else None
        
        response = requests.post(
            f"{API_URL}/mascotas/",
            json={
                "cliente_id": cliente_id,
                "nombre": nombre,
                "especie": especie,
                "raza": raza,
                "fecha_nacimiento": fecha_nacimiento_str,
                "edad": edad,
                "peso": peso,
                "sexo": sexo,
                "alergias": alergias,
                "condiciones_especiales": condiciones_especiales
            }
        )
        
        if response.status_code == 201:
            st.success("Mascota registrada exitosamente")
            return True
        else:
            st.error(f"Error al registrar la mascota: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

def actualizar_mascota(mascota_id, datos):
    """Actualizar información de una mascota"""
    try:
        response = requests.put(f"{API_URL}/mascotas/{mascota_id}", json=datos)
        if response.status_code == 200:
            st.success("Información actualizada exitosamente")
            return True
        else:
            st.error("Error al actualizar la información")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

def eliminar_mascota(mascota_id):
    """Eliminar una mascota"""
    try:
        response = requests.delete(f"{API_URL}/mascotas/{mascota_id}")
        if response.status_code in [200, 204]:
            st.success("Mascota eliminada exitosamente")
            return True
        else:
            st.error("Error al eliminar la mascota")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

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

def main():
    st.title("🐾 Gestión de Mascotas")
    
    # Crear pestañas para las diferentes opciones
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Registrar Mascota", "Lista de Mascotas", "Buscar Mascota", "Modificar Mascota", "Eliminar Mascota", "Vacunas"])

    with tab1:
        st.header("Registrar Mascota")
        cliente_id = st.text_input("ID del Cliente")
        nombre = st.text_input("Nombre de la Mascota")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"])
        raza = st .text_input("Raza")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento")
        edad = st.number_input("Edad (años)", min_value=0)
        peso = st.number_input("Peso (kg)", min_value=0.0)
        sexo = st.selectbox("Sexo", ["M", "H"])
        alergias = st.text_input("Alergias (opcional)")
        condiciones_especiales = st.text_input("Condiciones Especiales (opcional)")

        if st.button("Registrar"):
            registrar_mascota(cliente_id, nombre, especie, raza, fecha_nacimiento, edad, peso, sexo, alergias, condiciones_especiales)

    with tab2:
        st.header("Lista de Mascotas")
        mascotas = load_mascotas()
        
        if mascotas:
            df_mascotas = pd.DataFrame(mascotas)
            st.dataframe(df_mascotas)
        else:
            st.info("No hay mascotas registradas")  

    with tab3:
        st.header("Buscar Mascota")
        search_option = st.selectbox("Buscar por", ["ID de Cliente", "ID de Mascota"])
        
        if search_option == "ID de Cliente":
            cliente_id = st.text_input("Ingrese el ID del Cliente")
            if st.button("Buscar"):
                mascotas = get_mascotas_by_cliente(cliente_id)
                if mascotas:
                    for mascota in mascotas:
                        st.write(f"ID: {mascota['id']}, Nombre: {mascota['nombre']}")
                else:
                    st.info("No se encontraron mascotas para este cliente.")

        elif search_option == "ID de Mascota":
            mascota_id = st.text_input("Ingrese el ID de la Mascota")
            if st.button("Buscar"):
                mascota = get_mascota_details(mascota_id)
                if mascota:
                    st.write(f"Nombre: {mascota['nombre']}, Especie: {mascota['especie']}")
                else:
                    st.info("No se encontró la mascota.")

    with tab4:
        # Formulario para actualizar mascota
        st.write("### Actualizar Mascota")
        with st.form("actualizar_mascota_form"):
            mascota_id = st.number_input("ID de la Mascota", min_value=1, step=1)
            nombre = st.text_input("Nuevo Nombre")
            especie = st.selectbox("Nueva Especie", ["Perro", "Gato", "Otro"])
            raza = st.text_input("Nueva Raza")
            fecha_nacimiento = st.date_input("Nueva Fecha de Nacimiento", value=None)  # Campo para fecha de nacimiento
            edad = st.number_input("Nueva Edad (años)", min_value=0)
            peso = st.number_input("Nuevo Peso (kg)", min_value=0.0)
            sexo = st.selectbox("Nuevo Sexo", ["M", "H"])
            alergias = st.text_input("Nuevas Alergias (opcional)")
            condiciones_especiales = st.text_input("Nuevas Condiciones Especiales (opcional)")
        
            submitted = st.form_submit_button("Actualizar Mascota")
            if submitted:
                if not nombre or not especie or not raza or not edad or not peso or not sexo:
                    st.error("Por favor, complete todos los campos requeridos")
                else:
                    # Convertir fecha_nacimiento a string en formato ISO
                    fecha_nacimiento_str = fecha_nacimiento.isoformat() if fecha_nacimiento else None
                
                    # Crear un diccionario con los datos actualizados
                    datos_actualizados = {
                        "nombre": nombre,
                        "especie": especie,
                        "raza": raza,
                        "fecha_nacimiento": fecha_nacimiento_str,  # Asegúrate de que esto sea una cadena
                        "edad": edad,
                        "peso": peso,
                        "sexo": sexo,
                        "alergias": alergias,
                        "condiciones_especiales": condiciones_especiales
                    }
                
                    # Llamar a la función de actualización
                    if actualizar_mascota(mascota_id, datos_actualizados):
                        st.success("Mascota actualizada exitosamente")
                        st.rerun()
                    else:
                        st.error("Error al actualizar la mascota")
    with tab5:
        st.header("Eliminar Mascota")
        mascota_id = st.text_input("Ingrese el ID de la Mascota a eliminar")
        if st.button("Eliminar"):
            if st.checkbox(f"¿Está seguro de que desea eliminar la mascota con ID {mascota_id}?"):
                eliminar_mascota(mascota_id)

    with tab6:
        st.header("Vacunas")
        # Aquí puedes implementar la lógica para registrar y mostrar las vacunas de una mascota

if __name__ == "__main__":
    main()