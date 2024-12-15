# Usar una imagen base de Python optimizada
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias y las instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto donde correrá Streamlit
EXPOSE 8501

# Comando para iniciar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
