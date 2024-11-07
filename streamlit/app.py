import streamlit as st

# Título de la aplicación
st.title("Gestión de Clínica Veterinaria")

# Menú lateral para la navegación entre páginas
page = st.sidebar.selectbox("Selecciona una página", ["Clientes", "Citas", "Tratamientos", "Productos", "Dashboard"])

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
