# Usa una imagen base más pequeña si solo necesitas el servidor
FROM python:3.8-slim

# Establece la variable de entorno para que Python no genere archivos .pyc
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instala dependencias en una capa separada para optimizar la cache de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . /app

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Ejecuta Uvicorn, con parámetros adicionales para mejorar rendimiento en producción
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
