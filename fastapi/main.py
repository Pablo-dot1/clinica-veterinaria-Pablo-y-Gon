from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import create_db

# Crear las tablas de la base de datos
create_db()

# Crear la aplicación FastAPI
app = FastAPI(title="API Clínica Veterinaria")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(router)

# Si necesitas verificar que la aplicación está funcionando
@app.get("/")
async def root():
    return {"message": "API Clínica Veterinaria funcionando"}
