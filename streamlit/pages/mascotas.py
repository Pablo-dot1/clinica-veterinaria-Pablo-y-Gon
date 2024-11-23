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

def get_historial_medico(mascota_id):
    """Obtener historial médico de una mascota"""
    try:
        response = requests.get(f"{API_URL}/mascotas/{mascota_id}/historial")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener el historial médico")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def registrar_vacuna(mascota_id, datos_vacuna):
    """Registrar una nueva vacuna"""
    try:
        response = requests.post(
            f"{API_URL}/mascotas/{mascota_id}/vacunas",
            json=datos_vacuna
        )
        if response.status_code == 201:
            st.success("Vacuna registrada exitosamente")
            return True
        else:
            st.error("Error al registrar la vacuna")
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Registrar Mascota", "Lista de Mascotas", "Buscar Mascota", "Historial Médico", "Vacunas"])

    with tab1:
        st.header("Registrar Mascota")
        cliente_id = st.text_input("ID del Cliente")
        nombre = st.text_input("Nombre de la Mascota")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"])
        raza = st.text_input("Raza")
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
            # Crear un DataFrame de pandas para mostrar las mascotas
            df_mascotas = pd.DataFrame(mascotas)
            st.dataframe(df_mascotas)  # Mostrar la tabla de mascotas
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
                        if st.button(f"Modificar {mascota['nombre']}"):
                            # Formulario para modificar la mascota
                            with st.form(key=f"modificar_{mascota['id']}"):
                                nombre = st.text_input("Nombre", value=mascota['nombre'])
                                especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"], index=["Perro", "Gato", "Otro"].index(mascota['especie']))
                                raza = st.text_input("Raza", value=mascota['raza'])
                                fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=pd.to_datetime(mascota['fecha_nacimiento']).date())
                                edad = st.number_input("Edad (años)", min_value=0, value=mascota['edad'])
                                peso = st.number_input("Peso (kg)", min_value=0.0, value=mascota['peso'])
                                sexo = st.selectbox("Sexo", ["M", "H"], index=["M", "H"].index(mascota['sexo']))
                                alergias = st.text_input("Alergias (opcional)", value=mascota.get('alergias', ""))
                                condiciones_especiales = st.text_input("Condiciones Especiales (opcional)", value=mascota.get('condiciones_especiales', ""))
                                
                                if st.form_submit_button("Actualizar"):
                                    datos_actualizados = {
                                        "nombre": nombre,
                                        "especie": especie,
                                        "raza": raza,
                                        "fecha_nacimiento": fecha_nacimiento.isoformat(),
                                        "edad": edad,
                                        "peso": peso,
                                        "sexo": sexo,
                                        "alergias": alergias,
                                        "condiciones_especiales": condiciones_especiales
                                    }
                                    actualizar_mascota(mascota['id'], datos_actualizados)

                        if st.button(f"Eliminar {mascota['nombre']}"):
                            if st.checkbox(f"¿Está seguro de que desea eliminar {mascota['nombre']}?"):
                                eliminar_mascota(mascota['id'])

        elif search_option == "ID de Mascota":
            mascota_id = st.text_input("Ingrese el ID de la Mascota")
            if st.button("Buscar"):
                mascota = get_mascota_details(mascota_id)
                if mascota:
                    st.write(f"Nombre: {mascota['nombre']}, Especie: {mascota['especie']}")
                    if st.button("Modificar"):
                        # Formulario para modificar la mascota
                        with st.form(key=f"modificar_{mascota['id']}"):
                            nombre = st.text_input("Nombre", value=mascota['nombre'])
                            especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"], index=["Perro", "Gato", "Otro"].index(mascota['especie']))
                            raza = st.text_input("Raza", value=mascota['raza'])
                            fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=pd.to_datetime(mascota['fecha_nacimiento']).date())
                            edad = st.number_input("Edad (años)", min_value=0, value=mascota['edad'])
                            peso = st.number_input("Peso (kg)", min_value=0.0, value=mascota['peso'])
                            sexo = st.selectbox("Sexo", ["M", "H"], index=["M", "H"].index(mascota['sexo']))
                            alergias = st.text_input("Alergias (opcional)", value=mascota.get('alergias', ""))
                            condiciones_especiales = st.text_input("Condiciones Especiales (opcional)", value=mascota.get('condiciones_especiales', ""))
                            
                            if st.form_submit_button("Actualizar"):
                                datos_actualizados = {
                                    "nombre": nombre,
                                    "especie": especie,
                                    "raza": raza,
                                    "fecha_nacimiento": fecha_nacimiento.isoformat(),
                                    "edad": edad,
                                    "peso": peso,
                                    "sexo": sexo,
                                    "alergias": alergias,
                                    "condiciones_especiales": condiciones_especiales
                                }
                                actualizar_mascota(mascota['id'], datos_actualizados)

                    if st.button("Eliminar"):
                        if st.checkbox(f"¿Está seguro de que desea eliminar {mascota['nombre']}?"):
                            eliminar_mascota(mascota['id'])

    with tab4:
        st.header("Historial Médico")
        # Aquí puedes implementar la lógica para mostrar el historial médico de una mascota

    with tab5:
        st.header("Vacunas")
        # Aquí puedes implementar la lógica para registrar y mostrar las vacunas de una mascota

if __name__ == "__main__":
    main()