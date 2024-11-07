from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes import router  # Asegúrate de que 'routes.py' está en la misma carpeta
from database import engine  # Importa tu engine de base de datos
from models_db import Base  # Cambié la importación para que sea desde models_db

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servidor de datos de la clínica veterinaria",
    description="""Gestión de datos de clientes, mascotas, citas y tratamientos.""",
    version="0.1.0",
)

class FormData(BaseModel):
    date: str
    description: str
    option: str
    amount: float

@app.post("/envio/")
async def submit_form(data: FormData):
    return {"message": "Formulario recibido", "data": data}

# Incluir las rutas de clientes, mascotas, citas y tratamientos
app.include_router(router)
