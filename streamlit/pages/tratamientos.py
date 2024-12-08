import streamlit as st
import requests
import os
from datetime import datetime

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# Función para crear un nuevo tratamiento
def crear_tratamiento():
    st.header("Crear Tratamiento")
    
    # Campos del formulario con validación
    nombre = st.text_input("Nombre del Tratamiento", 
                          help="Ingrese el nombre del tratamiento (mínimo 2 caracteres)")
    
    descripcion = st.text_area("Descripción del Tratamiento",
                              help="Proporcione una descripción detallada del tratamiento")
    
    costo = st.number_input("Costo", 
                           min_value=0.0, 
                           step=0.1,
                           help="Ingrese el costo del tratamiento")
    
    duracion = st.number_input("Duración (días)", 
                              min_value=1,
                              help="Duración estimada del tratamiento en días")
    
    indicaciones = st.text_area("Indicaciones",
                               help="Indicaciones específicas para el tratamiento")

    if st.button("Crear Tratamiento"):
        if len(nombre) < 2:
            st.error("El nombre del tratamiento debe tener al menos 2 caracteres")
            return
            
        datos = {
            "nombre": nombre,
            "descripcion": descripcion,
            "costo": costo,
            "duracion": duracion,
            "indicaciones": indicaciones
        }
        
        respuesta = requests.post(f"{API_URL}/tratamientos/", json=datos)
        if respuesta.status_code == 201:
            st.success("¡Tratamiento creado exitosamente!")
            st.balloons()
        else:
            st.error(f"Error al crear el tratamiento: {respuesta.text}")

# Función para visualizar los tratamientos
def ver_tratamientos():
    st.header("Tratamientos Disponibles")
    
    # Añadir filtros
    filtro_nombre = st.text_input("Filtrar por nombre")
    
    respuesta = requests.get(f"{API_URL}/tratamientos/")
    if respuesta.status_code == 200:
        tratamientos = respuesta.json()
        
        # Aplicar filtro si existe
        if filtro_nombre:
            tratamientos = [t for t in tratamientos if filtro_nombre.lower() in t['nombre'].lower()]
        
        # Mostrar tratamientos en un formato más organizado
        for tratamiento in tratamientos:
            with st.expander(f"📋 {tratamiento['nombre']} - ${tratamiento['costo']}"):
                st.write(f"**Descripción:** {tratamiento['descripcion']}")
                st.write(f"**Duración:** {tratamiento.get('duracion', 'No especificada')} días")
                st.write(f"**Indicaciones:** {tratamiento.get('indicaciones', 'No especificadas')}")
                st.write(f"**ID:** {tratamiento['id']}")
    else:
        st.error("No se pudieron cargar los tratamientos. Por favor, intente más tarde.")

# Función para modificar un tratamiento
def modificar_tratamiento():
    st.header("Modificar Tratamiento")
    
    tratamiento_id = st.number_input("ID del Tratamiento", min_value=1)
    
    # Obtener datos actuales del tratamiento
    respuesta = requests.get(f"{API_URL}/tratamientos/{tratamiento_id}")
    if respuesta.status_code == 200:
        tratamiento_actual = respuesta.json()
        
        nombre = st.text_input("Nuevo Nombre del Tratamiento", value=tratamiento_actual.get('nombre', ''))
        descripcion = st.text_area("Nueva Descripción", value=tratamiento_actual.get('descripcion', ''))
        costo = st.number_input("Nuevo Costo", 
                               value=float(tratamiento_actual.get('costo', 0.0)),
                               min_value=0.0, 
                               step=0.1)
        duracion = st.number_input("Nueva Duración (días)", 
                                 value=int(tratamiento_actual.get('duracion', 1)),
                                 min_value=1)
        indicaciones = st.text_area("Nuevas Indicaciones", 
                                  value=tratamiento_actual.get('indicaciones', ''))

        if st.button("Modificar Tratamiento"):
            datos = {
                "nombre": nombre,
                "descripcion": descripcion,
                "costo": costo,
                "duracion": duracion,
                "indicaciones": indicaciones
            }
            
            respuesta = requests.put(f"{API_URL}/tratamientos/{tratamiento_id}", json=datos)
            if respuesta.status_code == 200:
                st.success("¡Tratamiento modificado correctamente!")
                st.balloons()
            else:
                st.error(f"Error al modificar el tratamiento: {respuesta.text }")
    else:
        st.error("No se encontró el tratamiento especificado")

# Función para eliminar un tratamiento
def eliminar_tratamiento():
    st.header("Eliminar Tratamiento")
    
    # Asignar un key único al number_input
    tratamiento_id = st.number_input("ID del Tratamiento", min_value=1, key="eliminar_tratamiento_id")
    
    if st.button("Eliminar Tratamiento"):
        # Confirmación de eliminación
        if st.checkbox("¿Está seguro de que desea eliminar este tratamiento?"):
            respuesta = requests.delete(f"{API_URL}/tratamientos/{tratamiento_id}")
            if respuesta.status_code in [200, 204]:  # Aceptar tanto 200 como 204
                st.success("Tratamiento eliminado correctamente")
            else:
                st.error(f"Error al eliminar el tratamiento: {respuesta.text}")  # Mostrar el mensaje de error
#funciones para vacunas

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

def load_veterinarios():
    """Cargar todos los veterinarios desde la API."""
    try:
        response = requests.get(f"{API_URL}/veterinarios/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al cargar veterinarios")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def registrar_vacuna(mascota_id, nombre_vacuna, fecha_aplicacion, fecha_proxima, veterinario_id, lote, notas):
    """Registrar una nueva vacuna."""
    try:
        response = requests.post(
            f"{API_URL}/mascotas/{mascota_id}/vacunas",
            json={
                "mascota_id": mascota_id,
                "nombre_vacuna": nombre_vacuna,
                "fecha_aplicacion": fecha_aplicacion,
                "fecha_proxima": fecha_proxima,
                "veterinario_id": veterinario_id,
                "lote": lote,
                "notas": notas
            }
        )
        if response.status_code == 201:
            st.success("Vacuna registrada exitosamente")
        else:
            st.error(f"Error al registrar la vacuna: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")

# Crear pestañas para las diferentes funciones
tabs = st.tabs(["Ver Tratamientos", "Crear Tratamiento", "Modificar Tratamiento", "Eliminar Tratamiento", "Vacunas"])

with tabs[0]:
    ver_tratamientos()

with tabs[1]:
    crear_tratamiento()

with tabs[2]:
    modificar_tratamiento()

with tabs[3]:
    eliminar_tratamiento()

with tabs[4]:
    # Registro de vacuna en la pestaña de vacunas
    st.title("Registrar Vacuna para Mascota")
    
    # Cargar datos necesarios
    mascotas = load_mascotas()
    veterinarios = load_veterinarios()

    if mascotas and veterinarios:
        with st.form("vacuna_form"):
            mascota_id = st.selectbox("Selecciona la Mascota", [m['id'] for m in mascotas])
            nombre_vacuna = st.text_input("Nombre de la Vacuna")
            fecha_aplicacion = st.date_input("Fecha de Aplicación", datetime.today())
            fecha_proxima = st.date_input("Fecha Próxima", datetime.today())
            veterinario_id = st.selectbox("Selecciona el Veterinario", [v['id'] for v in veterinarios])
            lote = st.text_input("Lote")
            notas = st.text_area("Notas (opcional)")

            submitted = st.form_submit_button("Registrar Vacuna")
            if submitted:
                if not nombre_vacuna or not lote:
                    st.error("Por favor, completa todos los campos requeridos")
                else:
                    registrar_vacuna(mascota_id, nombre_vacuna, fecha_aplicacion.isoformat(), fecha_proxima.isoformat(), veterinario_id, lote, notas)
    else:
        st.info("No hay mascotas o veterinarios registrados en la base de datos.")