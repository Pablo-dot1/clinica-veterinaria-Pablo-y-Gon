import streamlit as st
import requests
from datetime import date
import os
import pandas as pd
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
        response = requests.post(
            f"{API_URL}/mascotas/",
            json={
                "cliente_id": cliente_id,
                "nombre": nombre,
                "especie": especie,
                "raza": raza,
                "fecha_nacimiento": fecha_nacimiento,
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

def main():
    st.title("🐾 Gestión de Mascotas")
    
    # Menú principal
    menu = st.sidebar.selectbox(
        "Seleccione una opción",
        ["Ver Mascotas", "Registrar Mascota", "Buscar Mascota", "Historial Médico", "Vacunas"]
    )
    
    if menu == "Ver Mascotas":
        st.subheader("Lista de Mascotas")
        cliente_id = st.number_input("ID del Cliente", min_value=1, step=1)
        if st.button("Buscar Mascotas"):
            mascotas = get_mascotas_by_cliente(cliente_id)
            if mascotas:
                df = pd.DataFrame(mascotas)
                st.dataframe(df)
                
                # Opciones para cada mascota
                mascota_seleccionada = st.selectbox(
                    "Seleccione una mascota para más opciones",
                    [f"{m['nombre']} (ID: {m['id']})" for m in mascotas]
                )
                if mascota_seleccionada:
                    mascota_id = int(mascota_seleccionada.split("ID: ")[1].rstrip(")"))
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Ver Detalles"):
                            detalles = get_mascota_details(mascota_id)
                            if detalles:
                                st.json(detalles)
                    with col2:
                        if st.button("Eliminar Mascota"):
                            if st.checkbox("¿Está seguro?"):
                                if eliminar_mascota(mascota_id):
                                    st.rerun()
    
    elif menu == "Registrar Mascota":
        st.subheader("Registrar Nueva Mascota")
        with st.form("registro_mascota"):
            cliente_id = st.number_input("ID del Cliente", min_value=1, step=1)
            nombre = st.text_input("Nombre de la mascota")
            especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
            raza = st.text_input("Raza")
            fecha_nacimiento = st.date_input("Fecha de nacimiento")
            edad = st.number_input("Edad (años)", min_value=0, max_value=50)
            peso = st.number_input("Peso (kg)", min_value=0.1, max_value=200.0)
            sexo = st.selectbox("Sexo", ["M", "H"])
            alergias = st.text_area("Alergias conocidas")
            condiciones = st.text_area("Condiciones especiales")
            
            if st.form_submit_button("Registrar"):
                registrar_mascota(
                    cliente_id, nombre, especie, raza,
                    fecha_nacimiento.isoformat(), edad, peso,
                    sexo, alergias, condiciones
                )
    
    elif menu == "Buscar Mascota":
        st.subheader("Buscar Mascota")
        mascota_id = st.number_input("ID de la Mascota", min_value=1, step=1)
        if st.button("Buscar"):
            mascota = get_mascota_details(mascota_id)
            if mascota:
                with st.expander("Detalles de la Mascota", expanded=True):
                    st.json(mascota)
                    if st.button("Actualizar Información"):
                        # Formulario de actualización
                        with st.form("actualizar_mascota"):
                            nuevo_peso = st.number_input("Nuevo peso (kg)", value=mascota['peso'])
                            nuevas_alergias = st.text_area("Actualizar alergias", value=mascota.get('alergias', ''))
                            nuevas_condiciones = st.text_area("Actualizar condiciones", value=mascota.get('condiciones_especiales', ''))
                            
                            if st.form_submit_button("Guardar Cambios"):
                                datos_actualizados = {
                                    "peso": nuevo_peso,
                                    "alergias": nuevas_alergias,
                                    "condiciones_especiales": nuevas_condiciones
                                }
                                actualizar_mascota(mascota_id, datos_actualizados)
    
    elif menu == "Historial Médico":
        st.subheader("Historial Médico")
        mascota_id = st.number_input("ID de la Mascota", min_value=1, step=1)
        if st.button("Ver Historial"):
            historial = get_historial_medico(mascota_id)
            if historial:
                for registro in historial:
                    with st.expander(f"Consulta: {registro['fecha']}"):
                        st.write(f"**Diagnóstico:** {registro['diagnostico']}")
                        st.write(f"**Tratamiento:** {registro['tratamiento']}")
                        st.write(f"**Notas:** {registro['notas']}")
    
    elif menu == "Vacunas":
        st.subheader("Registro de Vacunas")
        mascota_id = st.number_input("ID de la Mascota", min_value=1, step=1)
        
        with st.form("registro_vacuna"):
            nombre_vacuna = st.text_input("Nombre de la Vacuna")
            fecha_aplicacion = st.date_input("Fecha de Aplicación")
            fecha_proxima = st.date_input("Fecha Próxima Aplicación")
            veterinario_id = st.number_input("ID del Veterinario", min_value=1)
            lote = st.text_input("Número de Lote")
            notas = st.text_area("Notas")
            
            if st.form_submit_button("Registrar Vacuna"):
                datos_vacuna = {
                    "nombre_vacuna": nombre_vacuna,
                    "fecha_aplicacion": fecha_aplicacion.isoformat(),
                    "fecha_proxima": fecha_proxima.isoformat(),
                    "veterinario_id": veterinario_id,
                    "lote": lote,
                    "notas": notas
                }
                registrar_vacuna(mascota_id, datos_vacuna)

if __name__ == "__main__":
    main()