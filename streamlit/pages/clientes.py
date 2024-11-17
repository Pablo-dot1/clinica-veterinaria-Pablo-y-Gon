import streamlit as st
import requests
import pandas as pd
import re
from datetime import datetime

API_URL = "http://fastapi:8000/clientes/"

def validar_telefono(telefono):
    """Valida el formato del número de teléfono"""
    patron = re.compile(r'^\+?[0-9]{9,15}$')
    return bool(patron.match(telefono))

def validar_email(email):
    """Valida el formato del email"""
    patron = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(patron.match(email)) if email else True

def get_clientes():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener clientes: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con el servidor: {str(e)}")
        return []

def crear_cliente():
    st.header("Crear Cliente")
    with st.form("crear_cliente_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre*", help="Nombre del cliente (requerido)")
            telefono = st.text_input("Teléfono*", help="Formato: +34XXXXXXXXX o XXXXXXXXX")
            email = st.text_input("Email", help="Opcional, debe ser un email válido")
            
        with col2:
            direccion = st.text_area("Dirección*", help="Dirección completa del cliente")
            notas = st.text_area("Notas adicionales", help="Información adicional relevante")
        
        submitted = st.form_submit_button("Crear Cliente", use_container_width=True)
        
        if submitted:
            # Validaciones
            errores = []
            if not nombre or len(nombre) < 2:
                errores.append("El nombre debe tener al menos 2 caracteres")
            if not telefono or not validar_telefono(telefono):
                errores.append("El teléfono no tiene un formato válido")
            if not direccion:
                errores.append("La dirección es requerida")
            if email and not validar_email(email):
                errores.append("El email no tiene un formato válido")
                
            if errores:
                for error in errores:
                    st.error(error)
                return
                
            data = {
                "nombre": nombre,
                "telefono": telefono,
                "direccion": direccion,
                "email": email,
                "notas": notas
            }
            
            try:
                with st.spinner('Creando cliente...'):
                    response = requests.post(API_URL, json=data)
                    if response.status_code == 201:
                        st.success("Cliente creado exitosamente")
                        st.balloons()
                    else:
                        st.error(f"Error al crear el cliente: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def ver_clientes():
    st.header("Lista de Clientes")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Buscar por nombre o teléfono")
    with col2:
        sort_by = st.selectbox("Ordenar por", ["Nombre", "Fecha de registro", "ID"])
    with col3:
        order = st.selectbox("Orden", ["Ascendente", "Descendente"])
    
    clientes = get_clientes()
    
    if not clientes:
        st.info("No hay clientes registrados")
        return
        
    # Filtrado
    filtered_clientes = clientes
    if search:
        filtered_clientes = [
            c for c in clientes 
            if search.lower() in c['nombre'].lower() or 
               search in c['telefono']
        ]
    
    # Ordenamiento
    if filtered_clientes:
        df = pd.DataFrame(filtered_clientes)
        
        if sort_by == "Nombre":
            df = df.sort_values('nombre', ascending=(order == "Ascendente"))
        elif sort_by == "Fecha de registro":
            df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
            df = df.sort_values('fecha_registro', ascending=(order == "Ascendente"))
        else:
            df = df.sort_values('id', ascending=(order == "Ascendente"))
        
        # Estilo personalizado para el DataFrame
        st.dataframe(
            df,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "nombre": "Nombre",
                "telefono": "Teléfono",
                "direccion": "Dirección",
                "email": "Email",
                "fecha_registro": st.column_config.DatetimeColumn(
                    "Fecha de Registro",
                    format="DD/MM/YYYY HH:mm"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.info(f"Mostrando {len(filtered_clientes)} de {len(clientes)} clientes")
    else:
        st.info("No se encontraron clientes con los criterios de búsqueda")

def modificar_cliente():
    st.header("Modificar Cliente")
    clientes = get_clientes()
    
    if not clientes:
        st.info("No hay clientes para modificar")
        return
        
    # Búsqueda para selección
    search_select = st.text_input("🔍 Buscar cliente para modificar")
    filtered_clientes = clientes
    if search_select:
        filtered_clientes = [
            c for c in clientes 
            if search_select.lower() in c['nombre'].lower() or 
               search_select in c['telefono']
        ]
    
    cliente_seleccionado = st.selectbox(
        "Seleccione el cliente a modificar",
        options=filtered_clientes,
        format_func=lambda x: f"{x['nombre']} - {x['telefono']}"
    )
    
    if cliente_seleccionado:
        with st.form("modificar_cliente_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre*", value=cliente_seleccionado['nombre'])
                telefono = st.text_input("Teléfono*", value=cliente_seleccionado['telefono'])
                email = st.text_input("Email", value=cliente_seleccionado.get('email', ''))
                
            with col2:
                direccion = st.text_area("Dirección*", value=cliente_seleccionado['direccion'])
                notas = st.text_area("Notas", value=cliente_seleccionado.get('notas', ''))
            
            submitted = st.form_submit_button("Actualizar Cliente", use_container_width=True)
            
            if submitted:
                # Validaciones
                errores = []
                if not nombre or len(nombre) < 2:
                    errores.append("El nombre debe tener al menos 2 caracteres")
                if not telefono or not validar_telefono(telefono):
                    errores.append("El teléfono no tiene un formato válido")
                if not direccion:
                    errores.append("La dirección es requerida")
                if email and not validar_email(email):
                    errores.append("El email no tiene un formato válido")
                    
                if errores:
                    for error in errores:
                        st.error(error)
                    return
                    
                data = {
                    "nombre": nombre,
                    "telefono": telefono,
                    "direccion": direccion,
                    "email": email,
                    "notas": notas
                }
                
                try:
                    with st.spinner('Actualizando cliente...'):
                        response = requests.put(
                            f"{API_URL}{cliente_seleccionado['id']}/",
                            json=data
                        )
                        if response.status_code == 200:
                            st.success("Cliente actualizado exitosamente")
                            st.balloons()
                        else:
                            st.error(f"Error al actualizar el cliente: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión: {str(e)}")

def eliminar_cliente():
    st.header("Eliminar Cliente")
    clientes = get_clientes()
    
    if not clientes:
        st.info("No hay clientes para eliminar")
        return
        
    # Búsqueda para selección
    search_delete = st.text_input("🔍 Buscar cliente para eliminar")
    filtered_clientes = clientes
    if search_delete:
        filtered_clientes = [
            c for c in clientes 
            if search_delete.lower() in c['nombre'].lower() or 
               search_delete in c['telefono']
        ]
    
    cliente_seleccionado = st.selectbox(
        "Seleccione el cliente a eliminar",
        options=filtered_clientes,
        format_func=lambda x: f"{x['nombre']} - {x['telefono']}"
    )
    
    if cliente_seleccionado:
        st.warning(
            f"¿Está seguro de que desea eliminar al cliente {cliente_seleccionado['nombre']}? "
            "Esta acción no se puede deshacer."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            confirmar = st.checkbox("Confirmo que deseo eliminar este cliente")
        with col2:
            if confirmar:
                if st.button("Eliminar Cliente", type="primary"):
                    try:
                        with st.spinner('Eliminando cliente...'):
                            response = requests.delete(
                                f"{API_URL}{cliente_seleccionado['id']}/"
                            )
                            if response.status_code == 204:
                                st.success("Cliente eliminado exitosamente")
                            else:
                                st.error(f"Error al eliminar el cliente: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error de conexión: {str(e)}")

def main():
    st.title("Gestión de Clientes")
    
    menu_options = {
        "Ver Clientes": ver_clientes,
        "Crear Cliente": crear_cliente,
        "Modificar Cliente": modificar_cliente,
        "Eliminar Cliente": eliminar_cliente
    }
    
    # Menú con iconos
    opcion = st.sidebar.selectbox(
        "Selecciona una acción",
        list(menu_options.keys()),
        format_func=lambda x: f"👥 {x}" if x == "Ver Clientes"
        else f"➕ {x}" if x == "Crear Cliente"
        else f"✏️ {x}" if x == "Modificar Cliente"
        else f"🗑️ {x}"
    )
    
    # Ejecutar la función seleccionada
    menu_options[opcion]()

if __name__ == "__main__":
    main()