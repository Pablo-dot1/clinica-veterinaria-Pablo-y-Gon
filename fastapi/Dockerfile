# Usa la imagen base de tiangolo/uvicorn-gunicorn-fastapi
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Crea el directorio de trabajo y copia el archivo requirements.txt
WORKDIR /fastapi
COPY requirements.txt .

# Instala las dependencias y psutil directamente
RUN pip install --no-cache-dir -r requirements.txt && pip install psutil

# Copia el resto de los archivos al contenedor
COPY . .

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Ejecuta Uvicorn, especificando el módulo y la aplicación, con ajustes para producción
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]