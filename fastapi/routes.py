from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db  # Esto debe estar configurado en tu archivo database.py
from models_db import ClienteDB, MascotaDB, CitaDB, TratamientoDB  # Importa los modelos de base de datos
from models import Cliente, Mascota, Cita, Tratamiento  # Pydantic para validación de datos

router = APIRouter()

# Rutas existentes para Clientes y Mascotas
@router.post("/clientes/")
async def crear_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    db_cliente = ClienteDB(**cliente.dict())  # Crear instancia de modelo DB
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/")
async def leer_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = db.query(ClienteDB).offset(skip).limit(limit).all()  # Consultar DB con ClienteDB
    return clientes

@router.post("/mascotas/")
async def crear_mascota(mascota: Mascota, db: Session = Depends(get_db)):
    db_mascota = MascotaDB(**mascota.dict())  # Crear instancia de modelo DB
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/mascotas/")
async def leer_mascotas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    mascotas = db.query(MascotaDB).offset(skip).limit(limit).all()  # Consultar DB con MascotaDB
    return mascotas

# Nuevas rutas para Citas
@router.post("/citas/")
async def crear_cita(cita: Cita, db: Session = Depends(get_db)):
    db_cita = CitaDB(**cita.dict())  # Crear instancia de modelo DB
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.get("/citas/")
async def leer_citas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    citas = db.query(CitaDB).offset(skip).limit(limit).all()  # Consultar DB con CitaDB
    return citas

# Nuevas rutas para Tratamientos
@router.post("/tratamientos/")
async def crear_tratamiento(tratamiento: Tratamiento, db: Session = Depends(get_db)):
    db_tratamiento = TratamientoDB(**tratamiento.dict())  # Crear instancia de modelo DB
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

@router.get("/tratamientos/")
async def leer_tratamientos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tratamientos = db.query(TratamientoDB).offset(skip).limit(limit).all()  # Consultar DB con TratamientoDB
    return tratamientos
