import streamlit as st
import requests
import matplotlib.pyplot as plt

# Gráficos interactivos para estadísticas
def generar_dashboard():
    st.header("Dashboard de la Clínica Veterinaria")
    
    # Petición de datos a la API del backend
    response_citas = requests.get("http://localhost:8000/citas/")
    citas = response_citas.json()

    # Mostrar número de citas
    st.write(f"Número de citas registradas: {len(citas)}")
    
    # Gráfico de citas por mes (usando matplotlib, ejemplo)
    meses = [cita['fecha_hora'].split('-')[1] for cita in citas]
    conteo_meses = {str(i): meses.count(str(i)) for i in range(1, 13)}

    fig, ax = plt.subplots()
    ax.bar(conteo_meses.keys(), conteo_meses.values())
    ax.set_xlabel("Mes")
    ax.set_ylabel("Número de Citas")
    ax.set_title("Citas por Mes")
    st.pyplot(fig)

generar_dashboard()
