# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos de dependencias
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el contenido de la carpeta local al contenedor
COPY app.py /app/app.py


# Expón el puerto en el que Streamlit se ejecuta
EXPOSE 8501

# Ejecuta la aplicación de Streamlit
CMD ["streamlit", "run", "app.py"]
