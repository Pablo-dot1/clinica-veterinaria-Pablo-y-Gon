import streamlit as st
import requests
from datetime import datetime, time, timedelta
import pytz
from typing import Optional

API_URL_CITAS = "http://fastapi:8000/citas/"
API_URL_MASCOTAS = "http://fastapi:8000/mascotas/"
API_URL_VETERINARIOS = "http://fastapi:8000/veterinarios/"

def get_mascota_nombre(mascota_id: int) -> Optional[str]:
    """Obtener el nombre de la mascota por ID"""
    try:
        response = requests.get(f"{API_URL_MASCOTAS}{mascota_id}")
        if response.status_code == 200:
            mascota = response.json()
            return mascota['nombre']
    except:
        return None
    return None

def get_veterinario_nombre(vet_id: int) -> Optional[str]:
    """Obtener el nombre del veterinario por ID"""
    try:
        response = requests.get(f"{API_URL_VETERINARIOS}{vet_id}")
        if response.status_code == 200:
            vet = response.json()
            return f"{vet['nombre']} {vet['apellido']}"
    except:
        return None
    return None

def validar_horario_laboral(hora):
    """Validar que la hora esté dentro del horario laboral (9:00 - 18:00)"""
    return time(9, 0) <= hora <= time(18, 0)

def crear_cita():
    st.header("Crear Cita")
    
    # Obtener lista de mascotas y veterinarios antes del formulario
    try:
        response_mascotas = requests.get(API_URL_MASCOTAS)
        response_veterinarios = requests.get(API_URL_VETERINARIOS)
        
        if response_mascotas.status_code != 200 or response_veterinarios.status_code != 200:
            st.error("Error al cargar las mascotas y veterinarios. Por favor, intente más tarde.")
            return
            
        mascotas = response_mascotas.json()
        veterinarios = response_veterinarios.json()
        
        # Crear opciones para los selectbox
        opciones_mascotas = {f"{m['nombre']} (ID: {m['id']})": m['id'] for m in mascotas}
        opciones_veterinarios = {f"{v['nombre']} {v['apellido']} (ID: {v['id']})": v['id'] for v in veterinarios}
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al servidor: {str(e)}")
        return
    
    with st.form(key="formulario_cita"):
        mascota_seleccionada = st.selectbox(
            "Seleccione la mascota",
            options=list(opciones_mascotas.keys()),
            help="Seleccione la mascota para la cita"
        )
        mascota_id = opciones_mascotas[mascota_seleccionada]
        
        veterinario_seleccionado = st.selectbox(
            "Seleccione el veterinario",
            options=list(opciones_veterinarios.keys()),
            help="Seleccione el veterinario para la cita"
        )
        veterinario_id = opciones_veterinarios[veterinario_seleccionado]
        
        # Validación de fecha y hora
        col1, col2 = st.columns(2)
        with col1:
            fecha_actual = datetime.now().date()
            fecha = st.date_input(
                "Fecha de la Cita",
                min_value=fecha_actual,
                help="Seleccione una fecha igual o posterior a hoy"
            )
        
        with col2:
            hora = st.time_input(
                "Hora de la Cita",
                value=time(9, 0),
                help="Seleccione una hora entre 9:00 AM y 6:00 PM"
            )
        
        if not validar_horario_laboral(hora):
            st.warning("⚠️ El horario de atención es de 9:00 AM a 6:00 PM")
        
        # Validación del motivo
        motivo = st.text_area(
            "Motivo de la Cita",
            help="Describa el motivo de la consulta (mínimo 5 caracteres)",
            max_chars=200
        )
        
        # Notas adicionales (opcional)
        notas = st.text_area(
            "Notas adicionales (opcional)",
            help="Agregue cualquier información adicional relevante",
            max_chars=500
        )
        
        submitted = st.form_submit_button("Crear Cita")
        
        if submitted:
            if len(motivo.strip()) < 5:
                st.error("❌ El motivo debe tener al menos 5 caracteres")
                return
                
            if not validar_horario_laboral(hora):
                st.error("❌ La hora seleccionada está fuera del horario de atención")
                return
                
            fecha_hora = datetime.combine(fecha, hora)
            
            with st.spinner("Creando cita..."):
                data = {
                    "mascota_id": mascota_id,
                    "veterinario_id": veterinario_id,
                    "fecha": fecha_hora.isoformat(),
                    "motivo": motivo.strip(),
                    "estado": "pendiente",
                    "notas": notas.strip() if notas else None
                }
                
                try:
                    response = requests.post(API_URL_CITAS, json=data)
                    if response.status_code == 201:
                        st.success("✅ ¡Cita creada exitosamente!")
                        st.balloons()
                        # Mostrar resumen de la cita
                        st.info(f"""
                        **Resumen de la cita:**
                        - 🐾 Mascota: {mascota_seleccionada}
                        - 👨‍⚕️ Veterinario: {veterinario_seleccionado}
                        - 📅 Fecha: {fecha.strftime('%d/%m/%Y')}
                        - 🕒 Hora: {hora.strftime('%H:%M')}
                        """)
                    else:
                        error_detail = response.json().get('detail', 'Error desconocido')
                        st.error(f"❌ Error al crear la cita: {error_detail}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
                except ValueError as e:
                    st.error(f"❌ Error en el formato de los datos: {str(e)}")

def ver_citas():
    st.header("Citas")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_fecha = st.date_input("Filtrar por fecha", None)
    with col2:
        estados = ["todos", "pendiente", "completada", "cancelada"]
        filtro_estado = st.selectbox("Filtrar por estado", estados)
    with col3:
        buscar = st.text_input("Buscar", placeholder="Buscar por ID o motivo...")
    
    try:
        with st.spinner("Cargando citas..."):
            response = requests.get(API_URL_CITAS)
            if response.status_code == 200:
                citas = response.json()
                
                # Aplicar filtros
                citas_filtradas = []
                for cita in citas:
                    fecha_cita = datetime.fromisoformat(cita['fecha'].replace('Z', '+00:00')).date()
                    
                    # Aplicar filtros
                    if filtro_fecha and fecha_cita != filtro_fecha:
                        continue
                    if filtro_estado != "todos" and cita['estado'] != filtro_estado:
                        continue
                    if buscar and not (
                        str(cita['id']).find(buscar) != -1 or 
                        cita['motivo'].lower().find(buscar.lower()) != -1
                    ):
                        continue
                        
                    citas_filtradas.append(cita)
                
                if not citas_filtradas:
                    st.info("📝 No hay citas que coincidan con los filtros seleccionados")
                else:
                    st.success(f"Se encontraron {len(citas_filtradas)} citas")
                    for cita in citas_filtradas:
                        with st.expander(
                            f"Cita #{cita['id']} - {datetime.fromisoformat(cita['fecha'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')}"
                        ):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("🆔 **ID:** ", cita['id'])
                                st.write("📅 **Fecha:** ", datetime.fromisoformat(cita['fecha'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M'))
                                st.write("🐾 **Mascota:** ", get_mascota_nombre(cita['mascota_id']) or f"ID: {cita['mascota_id']}")
                            with col2:
                                st.write("👨‍⚕️ **Veterinario:** ", get_veterinario_nombre(cita['veterinario_id']) or f"ID: {cita['veterinario_id']}")
                                st.write("📋 **Estado:** ", cita['estado'])
                                st.write("ℹ️ **Motivo:** ", cita['motivo'])
                            
                            if cita['notas']:
                                st.write("📝 **Notas:** ", cita['notas'])
                            
                            # Botones de acción según el estado
                            if cita['estado'] == 'pendiente':
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("✅ Completar", key=f"completar_{cita['id']}"):
                                        try:
                                            update_response = requests.put(
                                                f"{API_URL_CITAS}{cita['id']}/estado",
                                                json={"estado": "completada"}
                                            )
                                            if update_response.status_code == 200:
                                                st.success("Estado actualizado correctamente")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error al actualizar el estado: {str(e)}")
                                with col2:
                                    if st.button("❌ Cancelar", key=f"cancelar_{cita['id']}"):
                                        try:
                                            update_response = requests.put(
                                                f"{API_URL_CITAS}{cita['id']}/estado",
                                                json={"estado": "cancelada"}
                                            )
                                            if update_response.status_code == 200:
                                                st.success("Cita cancelada correctamente")
                                                st.rerun()
                                        except Exception as e:
                                            st.error(f"Error al cancelar la cita: {str(e)}")
            else:
                error_detail = response.json().get('detail', 'Error desconocido')
                st.error(f"No se pudieron cargar las citas: {error_detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {str(e)}")
    except Exception as e:
        st.error(f"Error al procesar los datos: {str(e)}")

# Menú principal
st.title("🗓️ Gestión de Citas")
opcion = st.sidebar.selectbox(
    "Selecciona una acción",
    ["Ver Citas", "Crear Cita"],
    help="Escoge la acción que deseas realizar"
)

if opcion == "Crear Cita":
    crear_cita()
else:
    ver_citas()