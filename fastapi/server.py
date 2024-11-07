from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routes import router  # Asegúrate de que 'routes.py' está en la misma carpeta

# Crea una instancia de FastAPI
app = FastAPI(
    title="Servidor de datos de la clínica veterinaria",
    description="Gestión de datos de clientes, mascotas, citas y tratamientos.",
    version="0.1.0",
)

# Definir el modelo para el formulario
class FormData(BaseModel):
    date: str
    description: str
    option: str
    amount: float

# Endpoint para recibir un formulario
@app.post("/envio/")
async def submit_form(data: FormData):
    return {"message": "Formulario recibido", "data": data}

# Incluir las rutas de clientes, mascotas, citas y tratamientos
app.include_router(router)
