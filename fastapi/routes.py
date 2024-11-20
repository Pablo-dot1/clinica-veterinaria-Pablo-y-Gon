from fastapi import APIRouter, HTTPException, Depends, Response, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import (
    Cliente, Cita, CitaCreate, CitaUpdate, Veterinario, ClienteCreate,
    Producto, Tratamiento
)
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

@router.get("/veterinarios/", response_model=List[Veterinario])
async def get_veterinarios(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los veterinarios con paginación
    """
    try:
        veterinarios = crud.get_veterinarios(db, skip=skip, limit=limit)
        if not veterinarios:
            logger.info("No se encontraron veterinarios en la base de datos")
            return []
        return veterinarios
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener veterinarios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener veterinarios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
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

@router.post("/clientes/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente
    """
    try:
        db_cliente = crud.create_cliente(db, cliente)
        return db_cliente
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el cliente en la base de datos"
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear cliente: {str(e)}")
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

# Rutas para Productos
@router.get("/productos/", response_model=List[Producto])
async def get_productos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los productos con paginación
    """
    try:
        productos = crud.get_productos(db, skip=skip, limit=limit)
        return productos
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener productos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )

@router.post("/productos/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_producto(producto: Producto, db: Session = Depends(get_db)):
    """
    Crear un nuevo producto
    """
    try:
        return crud.create_producto(db, producto)
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear producto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )

@router.put("/productos/{producto_id}", response_model=Producto)
async def update_producto(
    producto_id: int,
    stock: int = Query(..., ge=0, description="Nuevo stock del producto"),
    db: Session = Depends(get_db)
):
    """
    Actualizar el stock de un producto
    """
    try:
        return crud.update_producto_stock(db, producto_id, stock)
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar stock: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el stock"
        )

@router.post("/productos/venta", status_code=status.HTTP_200_OK)
async def registrar_venta(
    producto_id: int = Query(..., description="ID del producto"),
    cantidad: int = Query(..., gt=0, description="Cantidad vendida"),
    db: Session = Depends(get_db)
):
    """
    Registrar una venta de producto
    """
    try:
        return crud.registrar_venta_producto(db, producto_id, cantidad)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al registrar venta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar la venta"
        )

# Rutas para Tratamientos
@router.get("/tratamientos/", response_model=List[Tratamiento])
async def get_tratamientos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los tratamientos con paginación
    """
    try:
        tratamientos = crud.get_tratamientos(db, skip=skip, limit=limit)
        return tratamientos
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tratamientos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )

@router.post("/tratamientos/", response_model=Tratamiento, status_code=status.HTTP_201_CREATED)
async def create_tratamiento(tratamiento: Tratamiento, db: Session = Depends(get_db)):
    """
    Crear un nuevo tratamiento
    """
    try:
        return crud.create_tratamiento(db, tratamiento)
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear tratamiento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el tratamiento"
        )

@router.put("/tratamientos/{tratamiento_id}", response_model=Tratamiento)
async def update_tratamiento(
    tratamiento_id: int,
    tratamiento: Tratamiento,
    db: Session = Depends(get_db)
):
    """
    Actualizar un tratamiento existente
    """
    try:
        return crud.update_tratamiento(db, tratamiento_id, tratamiento)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar tratamiento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el tratamiento"
        )

@router.delete("/tratamientos/{tratamiento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un tratamiento
    """
    try:
        if not crud.delete_tratamiento(db, tratamiento_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tratamiento no encontrado"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar tratamiento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el tratamiento"
        )

# Rutas adicionales para Clientes
@router.put("/clientes/{cliente_id}", response_model=Cliente)
async def update_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un cliente existente
    """
    try:
        return crud.update_cliente(db, cliente_id, cliente)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el cliente"
        )

@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un cliente
    """
    try:
        if not crud.delete_cliente(db, cliente_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el cliente"
        )