import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

def load_citas_con_clientes():
    try:
        response = requests.get(f"{API_URL}/citas/con-clientes/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar citas: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def load_citas(estado=None):
    try:
        if estado and estado != "Todas":
            citas_con_clientes = load_citas_con_clientes()
            citas_filtradas = [(cita, cliente) for cita, cliente in citas_con_clientes if cita['estado'] == estado]
            return citas_filtradas
        else:
            return load_citas_con_clientes()
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def load_clientes():
    try:
        response = requests.get(f"{API_URL}/clientes/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al cargar clientes")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def load_mascotas(cliente_id):
    try:
        response = requests.get(f"{API_URL}/mascotas/cliente/{cliente_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar mascotas: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

def load_veterinarios():
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

def cancelar_cita(cita_id):
    try:
        response = requests.put(
            f"{API_URL}/citas/{cita_id}",
            json={"estado": "cancelada"}
        )
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cancelar la cita: {str(e)}")
        return False
def aceptar_cita(cita_id):
    """Aceptar una cita y cambiar su estado a Confirmada."""
    try:
        response = requests.put(f"{API_URL}/citas/{cita_id}", json={"estado": "confirmada"})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        st.error(f"Error al aceptar la cita: {str(e)}")
        return False

def completar_cita(cita_id):
    """Completar una cita y cambiar su estado a Completada."""
    try:
        # Asegúrate de usar la ruta correcta para completar la cita
        response = requests.put(f"{API_URL}/citas/{cita_id}/completar")
        
        if response.status_code == 200:
            return response.json()  # Retorna la cita completada
        else:
            st.error(f"Error al completar la cita: {response.status_code} - {response.text}")
            print(f"Error al completar la cita: {response.status_code} - {response.text}")  # Imprimir en consola
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error al completar la cita: {str(e)}")
        print(f"Error de conexión: {str(e)}")  # Imprimir en consola
        return False

def load_tratamientos():
    try:
        response = requests.get(f"{API_URL}/tratamientos/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al cargar tratamientos: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
        return []

st.title("Gestión de Citas")

# Tabs para organizar la interfaz
tab1, tab2 = st.tabs(["Ver Citas", "Programar Cita"])

with tab1:
    # Filtros para citas
    st.subheader("Filtrar Citas")
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha inicio", datetime.now())
    with col2:
        fecha_fin = st.date_input("Fecha fin", datetime.now() + timedelta(days=30))
    
    estado_filtro = st.selectbox(
        "Estado de la cita",
        ["Todas", "pendiente", "confirmada", "cancelada", "completada"]
    )

    # Cargar y mostrar citas
    citas = load_citas(estado=estado_filtro)
    if citas:
        st.write("### Lista de Citas")
        for cita, cliente in citas:
            with st.expander(f"Cita {cita['id']} - {cita['fecha']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Cliente:** {cliente['nombre']} {cliente['apellido']}")
                    st.write(f"**Veterinario ID:** {cita.get('veterinario_id', 'N/A')}")
                with col2:
                    st.write(f"**Fecha:** {cita.get('fecha', 'N/A')}")
                    st.write(f"**Estado:** {cita.get('estado', 'Pendiente')}")
                with col3:
                    # Lógica para mostrar botones según el estado de la cita
                    if cita['estado'] == 'pendiente':
                        if st.button("Aceptar", key=f"accept_{cita['id']}"):
                            # Lógica para aceptar la cita (cambiar estado a Confirmada)
                            if aceptar_cita(cita['id']):
                                st.success("Cita aceptada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al aceptar la cita")
                    
                        if st.button("Cancelar", key=f"cancel_{cita['id']}"):
                            if cancelar_cita(cita['id']):
                                st.success("Cita cancelada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al cancelar la cita")

                    elif cita['estado'] == 'confirmada':
                        if st.button("Cancelar", key=f"cancel_{cita['id']}"):
                            if cancelar_cita(cita['id']):
                                st.success("Cita cancelada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al cancelar la cita")

                        if st.button("Completar", key=f"complete_{cita['id']}"):
                            # Lógica para completar la cita (cambiar estado a Completada)
                            if completar_cita(cita['id']):
                                st.success("Cita completada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al completar la cita")

                # No se muestran botones para estados Cancelada o Completada
    else:
        st.info("No hay citas programadas")
with tab2:
    st.subheader("Programar Nueva Cita")
    
    # Cargar datos necesarios
    clientes = load_clientes()
    veterinarios = load_veterinarios()
    tratamientos = load_tratamientos()  # Cargar tratamientos si es necesario
    
    # Selección de cliente
    cliente_options = {f"{c['nombre']} ({c['email']})": c['id'] for c in clientes}
    cliente_id = st.selectbox("Cliente", options=list(cliente_options.keys()))
    
    # Botón para cargar los datos de las mascotas del cliente seleccionado
    if st.button("Cargar Mascotas del Cliente"):
        if cliente_options[cliente_id]:
            mascotas = load_mascotas(cliente_options[cliente_id])
            mascota_options = {f"{m['nombre']}": m['id'] for m in mascotas}
            st.session_state.mascota_options = mascota_options  # Guardar las opciones de mascotas en el estado de la sesión
            st.success("Mascotas cargadas exitosamente.")
        else:
            st.error("Por favor, seleccione un cliente válido.")
    
    with st.form("nueva_cita_form"):
        # Selección de mascota
        if 'mascota_options' in st.session_state:
            mascota_id = st.selectbox("Mascota", options=list(st.session_state.mascota_options.keys()))
        else:
            st.warning("Primero, cargue las mascotas del cliente seleccionado.")
        
        # Selección de veterinario
        veterinario_options = {f"{v['nombre']}": v['id'] for v in veterinarios}
        veterinario_id = st.selectbox("Veterinario", options=list(veterinario_options.keys()))
        
        # Fecha y hora
        fecha = st.date_input(
            "Fecha",
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=90)
        )
        hora = st.time_input("Hora")
        
        # Detalles adicionales
        motivo = st.text_area("Motivo de la cita")
        notas = st.text_area("Notas adicionales")
        tratamiento_id = st.selectbox("Tratamiento (opcional)", options=[None] + [t['id'] for t in tratamientos])
        
        submitted = st.form_submit_button("Programar Cita")
        if submitted:
            if not cliente_id or not veterinario_id or not mascota_id or not fecha or not hora or not motivo:
                st.error("Por favor, complete todos los campos requeridos")
            else:
                # Convertir fecha y hora a formato ISO
                fecha_hora = datetime.combine(fecha, hora)
                fecha_hora_iso = fecha_hora.isoformat()
                
                try:
                    response = requests.post(
                        f"{API_URL}/citas/",
                        json={
                            "cliente_id": cliente_options[cliente_id],
                            "veterinario_id": veterinario_options[veterinario_id],
                            "mascota_id": st.session_state.mascota_options[mascota_id],
                            "fecha": fecha_hora_iso,
                            "motivo": motivo,
                            "notas": notas,
                            "estado": "pendiente",
                            "tratamiento_id": tratamiento_id  # Asegúrate de incluir este campo si es necesario
                        }
                    )

                    if response.status_code == 201:
                        st.success("Cita programada exitosamente")

                    else:
                        st.error(f"Error al programar la cita: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")