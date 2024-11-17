from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models
import crud
from database import get_db
from fastapi import status
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Clínica Veterinaria"],
    responses={404: {"description": "No encontrado"}},
)

@router.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy"}

@router.get("/clientes/", response_model=List[models.Cliente])
async def get_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los clientes"""
    try:
        clientes = crud.get_clientes(db, skip=skip, limit=limit)
        if not clientes:
            return []
        return clientes
    except Exception as e:
        logger.error(f"Error al obtener clientes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/citas/", response_model=List[models.Cita])
async def get_citas(db: Session = Depends(get_db)):
    """Obtener todas las citas"""
    try:
        citas = crud.get_citas(db)
        if not citas:
            return []
        return citas
    except Exception as e:
        logger.error(f"Error al obtener citas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
