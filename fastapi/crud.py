from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status
import models
from db_models import (
    ClienteDB, VeterinarioDB, MascotaDB, HistorialMedicoDB,
    VacunaDB, CitaDB, TratamientoDB, MedicamentoDB,
    ProductoDB, FacturaDB, ReviewDB
)
from datetime import datetime
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# CRUD operations for Cliente
def get_cliente(db: Session, cliente_id: int):
    """
    Obtener un cliente por su ID con manejo de errores mejorado
    """
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )
        return cliente
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener cliente {cliente_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )

def get_cliente_by_email(db: Session, email: str):
    """
    Obtener un cliente por su email con validación mejorada
    """
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.email == email).first()
        if not cliente:
            logger.info(f"No se encontró cliente con email: {email}")
            return None
        return cliente
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al buscar cliente por email {email}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al buscar cliente por email"
        )

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener lista de clientes con paginación y manejo de errores mejorado
    """
    try:
        return db.query(ClienteDB).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener lista de clientes: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de clientes"
        )

def get_veterinarios(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener lista de veterinarios con paginación y manejo de errores
    """
    try:
        return db.query(VeterinarioDB).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener lista de veterinarios: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de veterinarios"
        )

def create_cliente(db: Session, cliente: models.ClienteCreate):
    """
    Crear un nuevo cliente con validaciones mejoradas
    """
    try:
        # Verificar si ya existe un cliente con el mismo email
        existing_cliente = get_cliente_by_email(db, cliente.email)
        if existing_cliente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con este email"
            )

        db_cliente = ClienteDB(**cliente.dict())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        logger.info(f"Cliente creado exitosamente: ID {db_cliente.id}")
        return db_cliente
    except IntegrityError as e:
        logger.error(f"Error de integridad al crear cliente: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos del cliente"
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear cliente: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el cliente en la base de datos"
        )

def get_citas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    estado: Optional[str] = None
):
    """
    Obtener citas con filtros mejorados y validación
    """
    try:
        query = db.query(CitaDB)

        if fecha_inicio:
            query = query.filter(CitaDB.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(CitaDB.fecha <= fecha_fin)
        if estado:
            query = query.filter(CitaDB.estado == estado)

        return query.offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener citas: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las citas"
        )

def create_cita(db: Session, cita: models.CitaCreate):
    """
    Crear una nueva cita con validaciones mejoradas
    """
    try:
        # Verificar si existen el cliente y el veterinario
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cita.cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cita.cliente_id} no encontrado"
            )

        veterinario = db.query(VeterinarioDB).filter(VeterinarioDB.id == cita.veterinario_id).first()
        if not veterinario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Veterinario con ID {cita.veterinario_id} no encontrado"
            )

        # Verificar si hay otras citas en el mismo horario
        citas_existentes = db.query(CitaDB).filter(
            CitaDB.veterinario_id == cita.veterinario_id,
            CitaDB.fecha == cita.fecha,
            CitaDB.estado != 'cancelada'
        ).first()

        if citas_existentes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El veterinario ya tiene una cita programada para esta fecha y hora"
            )

        db_cita = CitaDB(**cita.dict())
        db.add(db_cita)
        db.commit()
        db.refresh(db_cita)
        logger.info(f"Cita creada exitosamente: ID {db_cita.id}")
        return db_cita

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear cita: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la cita en la base de datos"
        )

def update_cita(db: Session, cita_id: int, cita: models.CitaUpdate):
    """
    Actualizar una cita existente con validaciones mejoradas
    """
    try:
        db_cita = db.query(CitaDB).filter(CitaDB.id == cita_id).first()
        if not db_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cita con ID {cita_id} no encontrada"
            )

        if cita.fecha and cita.fecha != db_cita.fecha:
            citas_existentes = db.query(CitaDB).filter(
                CitaDB.veterinario_id == db_cita.veterinario_id,
                CitaDB.fecha == cita.fecha,
                CitaDB.id != cita_id,
                CitaDB.estado != 'cancelada'
            ).first()

            if citas_existentes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El veterinario ya tiene una cita programada para esta fecha y hora"
                )

        for key, value in cita.dict(exclude_unset=True).items():
            setattr(db_cita, key, value)

        db.commit()
        db.refresh(db_cita)
        logger.info(f"Cita actualizada exitosamente: ID {cita_id}")
        return db_cita

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar cita {cita_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la cita"
        )

def delete_cita(db: Session, cita_id: int):
    """
    Eliminar una cita con validaciones mejoradas
    """
    try:
        db_cita = db.query(CitaDB).filter(CitaDB.id == cita_id).first()
        if not db_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cita con ID {cita_id} no encontrada"
            )

        # Usar el método puede_eliminar() para verificar si la cita puede ser eliminada
        cita_model = models.Cita.from_orm(db_cita)
        if not cita_model.puede_eliminar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar una cita completada"
            )

        db.delete(db_cita)
        db.commit()
        logger.info(f"Cita eliminada exitosamente: ID {cita_id}")
        return True

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar cita {cita_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la cita"
        )

# Funciones CRUD para Productos
def get_productos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener lista de productos con paginación
    """
    try:
        return db.query(ProductoDB).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener productos"
        )

def create_producto(db: Session, producto: models.Producto):
    """
    Crear un nuevo producto
    """
    try:
        db_producto = ProductoDB(**producto.dict(exclude={'id'}))
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except SQLAlchemyError as e:
        logger.error(f"Error al crear producto: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )

def update_producto_stock(db: Session, producto_id: int, stock: int):
    """
    Actualizar el stock de un producto
    """
    try:
        producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        producto.stock = stock
        db.commit()
        db.refresh(producto)
        return producto
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar stock del producto: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el stock"
        )

def registrar_venta_producto(db: Session, producto_id: int, cantidad: int):
    """
    Registrar una venta de producto
    """
    try:
        producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        if producto.stock < cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente"
            )
        producto.stock -= cantidad
        db.commit()
        db.refresh(producto)
        return {"mensaje": "Venta registrada exitosamente"}
    except SQLAlchemyError as e:
        logger.error(f"Error al registrar venta: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar la venta"
        )

def validate_producto_stock(db: Session, producto_id: int, cantidad: int):
    """
    Validar el stock de un producto
    """
    try:
        producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        if producto.stock < cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {producto.nombre}"
            )
        return producto
    except SQLAlchemyError as e:
        logger.error(f"Error al validar stock del producto {producto_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al verificar el stock del producto"
        )
def update_cliente(db: Session, cliente_id: int, cliente: models.ClienteCreate):
    """
    Actualizar un cliente existente.
    """
    try:
        db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
        if not db_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)

        db.commit()
        db.refresh(db_cliente)
        logger.info(f"Cliente actualizado exitosamente: ID {cliente_id}")
        return db_cliente

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al actualizar cliente {cliente_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el cliente en la base de datos"
        )
def delete_cliente(db: Session, cliente_id: int):
    """Eliminar un cliente por su ID."""
    try:
        db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
        if not db_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        db.delete(db_cliente)
        db.commit()
        logger.info(f"Cliente eliminado exitosamente: ID {cliente_id}")
        return {"detail": "Cliente eliminado exitosamente"}
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar cliente {cliente_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el cliente en la base de datos"
        )