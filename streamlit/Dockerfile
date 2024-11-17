# Usa una imagen base de Python
FROM python:3.11-slim

RUN mkdir /streamlit

# Copia los requisitos de dependencias
COPY requirements.txt /streamlit

WORKDIR /streamlit

# Limpia la caché de pip e instala las dependencias
RUN pip cache purge && \
    pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta local al contenedor
COPY . /streamlit

# Expón el puerto en el que Streamlit se ejecuta
EXPOSE 8501

# Ejecuta la aplicación de Streamlit
CMD ["streamlit", "run", "app.py"]
