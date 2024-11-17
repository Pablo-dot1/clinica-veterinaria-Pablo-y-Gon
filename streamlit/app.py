import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Clínica Veterinaria",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2.5rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .reportview-container {
        background: linear-gradient(to bottom right, #ffffff, #f0f2f6);
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
    }
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Título de la aplicación con mejor formato
st.markdown("""
    <div style='background-color: #ffffff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
        <h1 style='text-align: center; color: #34495e; margin-bottom: 0.5rem;'>
            🏥 Clínica Veterinaria Premium
        </h1>
        <p style='text-align: center; color: #7f8c8d; font-size: 1.2rem;'>
            Cuidando a tus mascotas con amor y profesionalismo
        </p>
    </div>
    """, unsafe_allow_html=True)

# Agregar imagen después del título
# Opción 1: Usando una URL de internet
st.image("https://images.pexels.com/photos/45170/kittens-cat-cat-puppy-rush-45170.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", width=700, caption="Nuestra Clínica")


# Menú lateral mejorado
with st.sidebar:
    st.image("https://img.icons8.com/fluency/240/000000/pet-commands-summon.png", width=120)
    st.markdown("""
        <div style='background-color: #34495e; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <h3 style='color: white; text-align: center; margin: 0;'>Menú Principal</h3>
        </div>
    """, unsafe_allow_html=True)
    page = st.selectbox(
        "",  # Eliminamos la etiqueta "Navegación"
        ["Dashboard", "Clientes", "Citas", "Tratamientos", "Productos"],
        format_func=lambda x: f"📊 {x}" if x == "Dashboard"
        else f"👥 {x}" if x == "Clientes"
        else f"📅 {x}" if x == "Citas"
        else f"💊 {x}" if x == "Tratamientos"
        else f"🏷️ {x}"
    )

# Redirigir al archivo correspondiente según la página seleccionada
if page == "Clientes":
    import pages.clientes
elif page == "Citas":
    import pages.citas
elif page == "Tratamientos":
    import pages.tratamientos
elif page == "Productos":
    import pages.productos
else:
    import pages.Dashboard

# Footer mejorado
st.markdown("""
    <div style='background-color: #34495e; padding: 1.5rem; border-radius: 10px; margin-top: 2rem;'>
        <div style='text-align: center; color: white;'>
            <p style='margin-bottom: 0.5rem;'>© 2024 Clínica Veterinaria Premium</p>
            <p style='font-size: 0.9rem; color: #bdc3c7;'>Cuidando la salud de tus mascotas con excelencia</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
