# Usar una imagen base de Python optimizada
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias y las instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear la carpeta de datos para la base de datos SQLite
RUN mkdir -p ./data

# Copiar el resto del código
COPY . .

# Exponer el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
