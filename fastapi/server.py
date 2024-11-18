# server.py
from main import app
from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir cualquier método HTTP
    allow_headers=["*"],  # Permitir cualquier cabecera HTTP
)
