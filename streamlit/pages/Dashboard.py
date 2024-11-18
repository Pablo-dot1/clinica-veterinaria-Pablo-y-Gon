import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# URL base de la API
API_URL = os.getenv('API_URL', 'http://localhost:8000')

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

def format_currency(value):
    return f"${value:,.2f}"

def generar_dashboard():
    st.markdown("""
        <h1 style='text-align: center; color: #2e6c80;'>
            📊 Dashboard de la Clínica Veterinaria
        </h1>
    """, unsafe_allow_html=True)

    # Contenedor para mostrar estado de conexión
    status_container = st.empty()

    # Obtener datos con indicador de carga
    with st.spinner('Cargando datos...'):
        citas = get_data("citas")
        productos = get_data("productos")
        clientes = get_data("clientes")
        tratamientos = get_data("tratamientos")

    if not any([citas, productos, clientes, tratamientos]):
        st.error("No se pudieron cargar los datos. Por favor, verifica la conexión con el servidor.")
        return

    # Mostrar estado de conexión
    status_container.success("Datos cargados correctamente")

    # Layout en columnas para KPIs
    st.markdown("### 📈 Indicadores Principales")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # Cálculo de KPIs
    total_citas = len(citas)
    total_clientes = len(clientes)
    productos_stock = sum([p.get('stock', 0) for p in productos])
    productos_bajo_stock = len([p for p in productos if p.get('stock', 0) < 10])

    with kpi1:
        st.metric(
            label="Total Citas",
            value=total_citas,
            delta=f"{total_citas - len([c for c in citas if datetime.strptime(c['fecha_hora'], '%Y-%m-%dT%H:%M:%S') < datetime.now() - timedelta(days=30)])} vs mes anterior"
        )
    with kpi2:
        st.metric(label="Total Clientes", value=total_clientes)
    with kpi3:
        st.metric(label="Productos en Stock", value=productos_stock)
    with kpi4:
        st.metric(
            label="Productos Bajo Stock",
            value=productos_bajo_stock,
            delta=-productos_bajo_stock,
            delta_color="inverse"
        )

    # Layout en columnas para gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de citas por mes
        if citas:
            df_citas = pd.DataFrame(citas)
            df_citas['fecha'] = pd.to_datetime(df_citas['fecha_hora'])
            df_citas['mes'] = df_citas['fecha'].dt.strftime('%Y-%m')
            citas_por_mes = df_citas['mes'].value_counts().sort_index()
            
            fig = px.line(
                x=citas_por_mes.index,
                y=citas_por_mes.values,
                title='Tendencia de Citas por Mes',
                labels={'x': 'Mes', 'y': 'Número de Citas'}
            )
            fig.update_layout(
                xaxis_title="Mes",
                yaxis_title="Número de Citas",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Gráfico de productos por categoría
        if productos:
            df_productos = pd.DataFrame(productos)
            productos_por_categoria = df_productos['categoria'].value_counts()
            
            fig = px.pie(
                values=productos_por_categoria.values,
                names=productos_por_categoria.index,
                title='Distribución de Productos por Categoría',
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Próximas citas
    st.markdown("### 📅 Próximas Citas")
    if citas:
        df_proximas_citas = pd.DataFrame([
            cita for cita in citas 
            if datetime.strptime(cita['fecha_hora'], '%Y-%m-%dT%H:%M:%S') > datetime.now()
        ])
        if not df_proximas_citas.empty:
            df_proximas_citas['fecha_hora'] = pd.to_datetime(df_proximas_citas['fecha_hora']).dt.strftime('%Y-%m-%d %H:%M')
            df_proximas_citas = df_proximas_citas.sort_values('fecha_hora').head()
            st.dataframe(
                df_proximas_citas[['fecha_hora', 'motivo', 'estado']],
                column_config={
                    "fecha_hora": "Fecha y Hora",
                    "motivo": "Motivo",
                    "estado": "Estado"
                },
                hide_index=True
            )
        else:
            st.info("No hay citas programadas próximamente")

    # Productos con bajo stock
    st.markdown("### ⚠️ Productos con Stock Bajo")
    if productos:
        productos_bajo_stock = [p for p in productos if p.get('stock', 0) < 10]
        if productos_bajo_stock:
            df_bajo_stock = pd.DataFrame(productos_bajo_stock)
            st.dataframe(
                df_bajo_stock[['nombre', 'stock', 'categoria']],
                column_config={
                    "nombre": "Nombre",
                    "stock": st.column_config.NumberColumn("Stock Actual"),
                    "categoria": "Categoría"
                },
                hide_index=True
            )
        else:
            st.success("No hay productos con stock bajo en este momento")

if __name__ == "__main__":
    generar_dashboard()
