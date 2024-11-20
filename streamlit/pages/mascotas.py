import streamlit as st
import requests
from datetime import date
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def verificar_cliente(cliente_id):
    """Verifica si existe un cliente con el ID proporcionado"""
    try:
        response = requests.get(f"{API_URL}/clientes/{cliente_id}")
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            st.error("El cliente especificado no existe en el sistema")
            return False
        else:
            st.error("Error al verificar el cliente. Por favor, intente nuevamente")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al verificar cliente: {str(e)}")
        return False

def registrar_mascota(cliente_id, nombre, especie, raza, fecha_nacimiento):
    """Registra una nueva mascota en el sistema"""
    try:
        # Primero verificar si el cliente existe
        if not verificar_cliente(cliente_id):
            return False  # El mensaje de error ya se muestra en verificar_cliente

        response = requests.post(
            f"{API_URL}/mascotas/",
            json={
                "cliente_id": cliente_id,
                "nombre": nombre,
                "especie": especie,
                "raza": raza,
                "fecha_nacimiento": fecha_nacimiento,
                "edad": 0,  # Se calculará en el backend
                "peso": 0.1,  # Peso mínimo por defecto
                "sexo": "M"  # Valor por defecto
            }
        )
        
        if response.status_code == 201:
            st.success("Mascota registrada exitosamente")
            return True
        elif response.status_code == 404:
            st.error("El cliente especificado no existe en el sistema")
            return False
        elif response.status_code == 422:
            error_detail = response.json().get('detail', 'Datos inválidos')
            st.error(f"Error de validación: {error_detail}")
            return False
        elif response.status_code == 409:
            st.error("Ya existe una mascota registrada con estos datos")
            return False
        else:
            st.error(f"Error inesperado al registrar la mascota (código {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return False

def main():
    st.title("Registro de Mascota")
    
    # Solicitar ID del cliente
    cliente_id = st.text_input("Ingrese el ID del cliente", key="cliente_id_input")
    
    # Verificar si se ingresó un ID de cliente
    if cliente_id and cliente_id.isdigit():
        # Convertir el ID a entero
        cliente_id = int(cliente_id)
        with st.form("registro_mascota_form"):
            st.write(f"Registrando mascota para el cliente ID: {cliente_id}")
            nombre = st.text_input("Nombre de la mascota")
            especie = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
            raza = st.text_input("Raza")
            fecha_nacimiento = st.date_input("Fecha de nacimiento", min_value=date(2000, 1, 1), max_value=date.today())
            
            submitted = st.form_submit_button("Registrar Mascota")
            if submitted:
                if not nombre or not especie or not raza:
                    st.error("Por favor, complete todos los campos")
                else:
                    if registrar_mascota(
                        int(cliente_id),
                        nombre,
                        especie,
                        raza,
                        fecha_nacimiento.isoformat()
                    ):
                        st.success("Mascota registrada exitosamente")
                        # Opción para registrar otra mascota para el mismo cliente
                        if st.button("Registrar otra mascota para este cliente"):
                            st.session_state["cliente_id_input"] = str(cliente_id)
                            st.experimental_rerun()
                        # Opción para registrar mascota para otro cliente
                        if st.button("Registrar mascota para otro cliente"):
                            st.session_state["cliente_id_input"] = ""
                            st.experimental_rerun()
                        # Opción para volver a la página de clientes
                        if st.button("Volver a Clientes"):
                            st.switch_page("pages/clientes.py")
    else:
        if cliente_id and not cliente_id.isdigit():
            st.error("Por favor, ingrese un ID de cliente válido (solo números)")

if __name__ == "__main__":
    main()