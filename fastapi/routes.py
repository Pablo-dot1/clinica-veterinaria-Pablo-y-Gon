from fastapi import APIRouter, HTTPException, Depends, Response, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import Cliente, Cita, CitaCreate, CitaUpdate
import crud
from database import get_db
from fastapi import status
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Clínica Veterinaria"],
    responses={
        404: {"description": "No encontrado"},
        500: {"description": "Error interno del servidor"},
        400: {"description": "Solicitud incorrecta"}
    },
)

@router.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    try:
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al verificar el estado del servicio"
        )

@router.get("/clientes/", response_model=List[Cliente])
async def get_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los clientes con paginación
    """
    try:
        clientes = crud.get_clientes(db, skip=skip, limit=limit)
        if not clientes:
            logger.info("No se encontraron clientes en la base de datos")
            return []
        return clientes
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener clientes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener clientes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/citas/", response_model=List[Cita])
async def get_citas(
    fecha_inicio: datetime = None,
    fecha_fin: datetime = None,
    estado: str = Query(None, regex="^(pendiente|confirmada|cancelada|completada)$"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las citas con filtros opcionales
    """
    try:
        # Validar fechas si se proporcionan
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha final"
            )

        citas = crud.get_citas(db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, estado=estado)
        if not citas:
            logger.info("No se encontraron citas con los criterios especificados")
            return []
        return citas
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener citas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al obtener citas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/citas/", response_model=Cita, status_code=status.HTTP_201_CREATED)
async def create_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva cita
    """
    try:
        # Validar que la fecha de la cita sea futura
        if cita.fecha <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de la cita debe ser futura"
            )

        return crud.create_cita(db, cita)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la cita en la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/citas/{cita_id}", response_model=Cita)
async def update_cita(
    cita_id: int,
    cita_update: CitaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una cita existente
    """
    try:
        # Validar fecha si se proporciona
        if cita_update.fecha and cita_update.fecha <= datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de actualización debe ser futura"
            )

        updated_cita = crud.update_cita(db, cita_id, cita_update)
        if not updated_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        return updated_cita
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la cita en la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al actualizar cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/citas/{cita_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una cita
    """
    try:
        if not crud.delete_cita(db, cita_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la cita de la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al eliminar cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
