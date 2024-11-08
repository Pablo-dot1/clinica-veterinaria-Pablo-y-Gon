# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router  # Importar el router desde routes.py

app = FastAPI()

# Permitir el acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir cualquier método HTTP
    allow_headers=["*"],  # Permitir cualquier cabecera HTTP
)

# Incluir las rutas del sistema de gestión
app.include_router(router)  # Usar el 'router' importado desde routes.py
