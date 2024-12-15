import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# URL base de la API
API_URL = os.getenv('API_URL', 'http://fastapi:8000')

def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener datos de {endpoint}: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al obtener {endpoint}: {str(e)}")
        return []

def generar_dashboard():
    st.title("📊 Dashboard de la Clínica Veterinaria")

    # Obtener datos
    citas = get_data("citas")
    productos = get_data("productos")
    clientes = get_data("clientes")
    mascotas = get_data("mascotas")  # Obtener datos de mascotas

    if not any([citas, productos, clientes, mascotas]):
        st.error("No se pudieron cargar los datos. Por favor, verifica la conexión con el servidor.")
        return

    # KPIs
    st.header("📈 Indicadores Principales")
    total_citas = len(citas)
    total_clientes = len(clientes)
    total_mascotas = len(mascotas)  # Total de mascotas
    total_citas_pendientes = len([cita for cita in citas if cita.get('estado') == 'pendiente'])  # Total de citas pendientes
    productos_stock = sum([p.get('stock', 0) for p in productos])
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Total Citas", total_citas)
    with col2:
        st.metric("Total Clientes", total_clientes)
    with col3:
        st.metric("Total Mascotas", total_mascotas)  # Mostrar total de mascotas
    with col4:
        st.metric("Citas Pendientes", total_citas_pendientes)  # Mostrar total de citas pendientes
    with col5:
        st.metric("Productos en Stock", productos_stock)
    # Gráfico de citas por mes
    st.header("📅 Tendencia de Citas por Mes")
    if citas:
        df_citas = pd.DataFrame(citas)

        # Asegúrate de que 'fecha' está en el DataFrame y convierte a datetime
        if 'fecha' in df_citas.columns:
            df_citas['fecha'] = pd.to_datetime(df_citas['fecha'], errors='coerce')
            df_citas['mes'] = df_citas['fecha'].dt.to_period('M')
            citas_por_mes = df_citas['mes'].value_counts().sort_index()

            fig_citas = px.line(
                x=citas_por_mes.index.astype(str),
                y=citas_por_mes.values,
                title='Tendencia de Citas por Mes',
                labels={'x': 'Mes', 'y': 'Número de Citas'}
            )
            st.plotly_chart(fig_citas)
        else:
            st.error("La clave 'fecha' no se encuentra en los datos de citas.")

    # Gráfico de productos por categoría
    st.header("📦 Distribución de Productos por Categoría")
    if productos:
        df_productos = pd.DataFrame(productos)
        productos_por_categoria = df_productos['categoria'].value_counts()

        fig_productos = px.pie(
            values=productos_por_categoria.values,
            names=productos_por_categoria.index,
            title='Distribución de Productos por Categoría',
            hole=0.4
        )
        st.plotly_chart(fig_productos)

    # Próximas citas
    st.header("📅 Próximas Citas")
    if citas:
        df_proximas_citas = pd.DataFrame([
            cita for cita in citas 
            if 'fecha' in cita and datetime.strptime(cita['fecha'], '%Y-%m-%dT%H:%M:%S') >= datetime.now()
        ])
        if not df_proximas_citas.empty:
            df_proximas_citas['fecha'] = pd.to_datetime(df_proximas_citas['fecha']).dt.strftime('%Y-%m-%d %H:%M')
            df_proximas_citas = df_proximas_citas.sort_values('fecha').head()
            st.dataframe(df_proximas_citas[['fecha', 'motivo', 'estado']])
    else:
            st.info("No hay citas programadas próximamente")

    

# Ejecutar la función para generar el dashboard
if __name__ == "__main__":
    generar_dashboard()