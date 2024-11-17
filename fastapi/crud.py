from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
import models
from db_models import (
    ClienteDB, VeterinarioDB, MascotaDB, HistorialMedicoDB,
    VacunaDB, CitaDB, TratamientoDB, MedicamentoDB,
    ProductoDB, FacturaDB, ReviewDB
)
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# CRUD operations for Cliente
def get_cliente(db: Session, cliente_id: int):
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    except Exception as e:
        logger.error(f"Error al obtener cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def get_cliente_by_email(db: Session, email: str):
    try:
        return db.query(ClienteDB).filter(ClienteDB.email == email).first()
    except Exception as e:
        logger.error(f"Error al buscar cliente por email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(ClienteDB).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error al obtener clientes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener la lista de clientes: {str(e)}")

def create_cliente(db: Session, cliente: models.ClienteCreate):
    try:
        db_cliente = ClienteDB(**cliente.dict())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")

# CRUD operations for Cita con mejor manejo de errores
def get_citas(db: Session, skip: int = 0, limit: int = 100):
    try:
        citas = db.query(CitaDB).offset(skip).limit(limit).all()
        if not citas:
            logger.info("No se encontraron citas")
            return []
        return citas
    except Exception as e:
        logger.error(f"Error al obtener citas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener las citas: {str(e)}")

def create_cita(db: Session, cita: models.CitaCreate):
    try:
        # Verificar si existen el cliente y el veterinario
        if not db.query(ClienteDB).filter(ClienteDB.id == cita.cliente_id).first():
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        if not db.query(VeterinarioDB).filter(VeterinarioDB.id == cita.veterinario_id).first():
            raise HTTPException(status_code=404, detail="Veterinario no encontrado")

        db_cita = CitaDB(**cita.dict())
        db.add(db_cita)
        db.commit()
        db.refresh(db_cita)
        return db_cita
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear cita: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear la cita: {str(e)}")


def update_cita(db: Session, cita_id: int, cita: models.CitaUpdate):
    db_cita = get_cita(db, cita_id)
    if not db_cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    for key, value in cita.dict(exclude_unset=True).items():
        setattr(db_cita, key, value)
    
    db.commit()
    db.refresh(db_cita)
    return db_cita

def delete_cita(db: Session, cita_id: int):
    db_cita = get_cita(db, cita_id)
    if not db_cita:
        return False
    
    db.delete(db_cita)
    db.commit()
    return True

def update_cita_estado(db: Session, cita_id: int, estado: str):
    db_cita = get_cita(db, cita_id)
    if not db_cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    db_cita.estado = estado
    db.commit()
    db.refresh(db_cita)
    return db_cita

# CRUD operations for Tratamiento
def get_tratamiento(db: Session, tratamiento_id: int):
    return db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()

def get_tratamientos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TratamientoDB).offset(skip).limit(limit).all()

def create_tratamiento(db: Session, tratamiento: models.Tratamiento):
    db_tratamiento = TratamientoDB(**tratamiento.dict())
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

# CRUD operations for Producto
def get_producto(db: Session, producto_id: int):
    return db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductoDB).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: models.Producto):
    db_producto = ProductoDB(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto_stock(db: Session, producto_id: int, cantidad: int):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_producto.stock += cantidad
    if db_producto.stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    
    db.commit()
    db.refresh(db_producto)
    return db_producto