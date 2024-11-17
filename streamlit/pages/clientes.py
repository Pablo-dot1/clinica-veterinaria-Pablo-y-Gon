import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/clientes/"

def get_clientes():
    try:
        response = requests.get(API_URL)
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        st.error("Error de conexión con el servidor")
        return []

def crear_cliente():
    st.header("Crear Cliente")
    with st.form("crear_cliente_form"):
        nombre = st.text_input("Nombre")
        telefono = st.text_input("Teléfono")
        direccion = st.text_input("Dirección")
        email = st.text_input("Email (opcional)")
        
        submitted = st.form_submit_button("Crear Cliente")
        
        if submitted:
            if not nombre or not telefono or not direccion:
                st.error("Por favor complete todos los campos obligatorios")
                return
                
            data = {
                "nombre": nombre,
                "telefono": telefono,
                "direccion": direccion,
                "email": email
            }
            
            try:
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
    clientes = get_clientes()
    
    if not clientes:
        st.info("No hay clientes registrados")
        return
        
    # Búsqueda
    search = st.text_input("🔍 Buscar cliente por nombre o teléfono")
    
    filtered_clientes = clientes
    if search:
        filtered_clientes = [
            c for c in clientes 
            if search.lower() in c['nombre'].lower() or 
               search in c['telefono']
        ]
    
    if filtered_clientes:
        df = pd.DataFrame(filtered_clientes)
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "nombre": "Nombre",
                "telefono": "Teléfono",
                "direccion": "Dirección",
                "email": "Email"
            },
            hide_index=True
        )
    else:
        st.info("No se encontraron clientes con los criterios de búsqueda")

def modificar_cliente():
    st.header("Modificar Cliente")
    clientes = get_clientes()
    
    if not clientes:
        st.info("No hay clientes para modificar")
        return
        
    cliente_seleccionado = st.selectbox(
        "Seleccione el cliente a modificar",
        options=clientes,
        format_func=lambda x: f"{x['nombre']} - {x['telefono']}"
    )
    
    with st.form("modificar_cliente_form"):
        nombre = st.text_input("Nombre", value=cliente_seleccionado['nombre'])
        telefono = st.text_input("Teléfono", value=cliente_seleccionado['telefono'])
        direccion = st.text_input("Dirección", value=cliente_seleccionado['direccion'])
        email = st.text_input("Email", value=cliente_seleccionado.get('email', ''))
        
        submitted = st.form_submit_button("Actualizar Cliente")
        
        if submitted:
            if not nombre or not telefono or not direccion:
                st.error("Por favor complete todos los campos obligatorios")
                return
                
            data = {
                "nombre": nombre,
                "telefono": telefono,
                "direccion": direccion,
                "email": email
            }
            
            try:
                response = requests.put(f"{API_URL}{cliente_seleccionado['id']}/", json=data)
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
        
    cliente_seleccionado = st.selectbox(
        "Seleccione el cliente a eliminar",
        options=clientes,
        format_func=lambda x: f"{x['nombre']} - {x['telefono']}"
    )
    
    if st.button("Eliminar Cliente"):
        if st.checkbox("¿Está seguro de que desea eliminar este cliente?"):
            try:
                response = requests.delete(f"{API_URL}{cliente_seleccionado['id']}/")
                if response.status_code == 204:
                    st.success("Cliente eliminado exitosamente")
                else:
                    st.error("Error al eliminar el cliente")
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
    
    opcion = st.sidebar.selectbox("Selecciona una acción", list(menu_options.keys()))
    menu_options[opcion]()

if __name__ == "__main__":
    main()
