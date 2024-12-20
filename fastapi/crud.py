from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status
import models
from db_models import (
    ClienteDB, VeterinarioDB, MascotaDB,
    VacunaDB, CitaDB, TratamientoDB,
    ProductoDB,FacturaDB
)
from datetime import datetime
import logging


# Configuración de logging
logger = logging.getLogger(__name__)

# CRUD operations for Cliente
def verificar_cliente(db: Session, cliente_id: int) -> bool:
    """
    Verifica si existe un cliente con el ID proporcionado
    """
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
        return cliente is not None
    except SQLAlchemyError as e:
        logger.error(f"Error al verificar cliente {cliente_id}: {str(e)}")
        return False

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
def get_veterinario(db: Session, veterinario_id: int):
    """
    Obtener un veterinario por su ID
    """
    try:
        veterinario = db.query(VeterinarioDB).filter(VeterinarioDB.id == veterinario_id).first()
        if not veterinario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Veterinario con ID {veterinario_id} no encontrado"
            )
        return veterinario
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener veterinario {veterinario_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
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

def get_citas(db: Session, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None, estado: Optional[str] = None):
    """Obtener citas con filtros opcionales."""
    try:
        query = db.query(CitaDB)

        if fecha_inicio:
            query = query.filter(CitaDB.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.filter(CitaDB.fecha <= fecha_fin)
        if estado:
            query = query.filter(CitaDB.estado == estado)

        citas = query.all()  # Devuelve todas las citas que coinciden con los filtros
        
        # Convertir a modelos Pydantic
        return [models.Cita.from_orm(cita) for cita in citas]  # Asegúrate de que esto devuelva una lista de objetos Cita
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener citas: {str(e)}")
        db.rollback()  # Asegúrate de revertir cualquier cambio en caso de error
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

def update_producto_stock(db: Session, producto_id: int, stock: int) -> ProductoDB:
    """ 
    Actualizar el stock de un producto por su ID. 
    """ 
    try:
        # Obtener el producto por ID
        producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Actualizar el stock
        producto.stock = stock
        db.commit()  # Guardar cambios en la base de datos
        db.refresh(producto)  # Refrescar el objeto para obtener los datos actualizados
        return producto  # Devolver el producto actualizado
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar stock del producto {producto_id}: {str(e)}")
        db.rollback()  # Revertir cambios en caso de error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el stock del producto"
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
def delete_producto(db: Session, producto_id: int) -> bool:
    """Eliminar un producto por su ID."""
    try:
        db_producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        if not db_producto:
            return False
        db.delete(db_producto)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al eliminar producto {producto_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el producto de la base de datos"
        )
#funciones cliente
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
    """
    Crear un nuevo veterinario con validaciones mejoradas
    """
    try:
        # Verificar si ya existe un veterinario con el mismo email
        existing_veterinario = db.query(VeterinarioDB).filter(VeterinarioDB.email == veterinario.email).first()
        if existing_veterinario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un veterinario con este email"
            )

        # Verificar si ya existe un veterinario con el mismo número colegiado
        existing_numero_colegiado = db.query(VeterinarioDB).filter(VeterinarioDB.numero_colegiado == veterinario.numero_colegiado).first()
        if existing_numero_colegiado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un veterinario con este número colegiado"
            )

        # Crear una nueva instancia de VeterinarioDB
        db_veterinario = VeterinarioDB(**veterinario.dict())
        db.add(db_veterinario)
        db.commit()
        db.refresh(db_veterinario)
        logger.info(f"Veterinario creado exitosamente: ID {db_veterinario.id}")
        return db_veterinario
    except IntegrityError as e:
        logger.error(f"Error de integridad al crear veterinario: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos del veterinario"
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al crear veterinario: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el veterinario en la base de datos"
        )

def get_mascota(db: Session, mascota_id: int):
    """
    Obtener una mascota por su ID
    """
    try:
        mascota = db.query(MascotaDB).filter(MascotaDB.id == mascota_id).first()
        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mascota con ID {mascota_id} no encontrada"
            )
        return mascota
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener mascota {mascota_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )

def get_mascotas_by_cliente(db: Session, cliente_id: int):
    """
    Obtener todas las mascotas de un cliente específico
    """
    try:
        mascotas = db.query(MascotaDB).filter(MascotaDB.cliente_id == cliente_id).all()
        if not mascotas:
            logger.info(f"No se encontraron mascotas para el cliente {cliente_id}")
            return []
        return mascotas
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener mascotas del cliente {cliente_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las mascotas del cliente"
        )



def create_mascota(db: Session, mascota: models.MascotaCreate):
    """
    Crear una nueva mascota
    """
    try:
        db_mascota = MascotaDB(**mascota.dict())
        db.add(db_mascota)
        db.commit()
        db.refresh(db_mascota)
        return db_mascota
    except SQLAlchemyError as e:
        logger.error(f"Error al crear mascota: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la mascota"
        )
def get_mascotas(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener lista de mascotas con paginación y manejo de errores mejorado
    """
    try:
        return db.query(MascotaDB).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener lista de mascotas: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de mascotas"
        )

def update_mascota(db: Session, mascota_id: int, mascota: models.MascotaCreate):
    """
    Actualizar una mascota existente
    """
    try:
        db_mascota = db.query(MascotaDB).filter(MascotaDB.id == mascota_id).first()
        if not db_mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mascota con ID {mascota_id} no encontrada"
            )
        
        for key, value in mascota.dict(exclude_unset=True).items():
            setattr(db_mascota, key, value)
        
        db.commit()
        db.refresh(db_mascota)
        return db_mascota
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar mascota: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la mascota"
        )

def delete_mascota(db: Session, mascota_id: int):
    """
    Eliminar una mascota
    """
    try:
        db_mascota = db.query(MascotaDB).filter(MascotaDB.id == mascota_id).first()
        if not db_mascota:
            return False
        db.delete(db_mascota)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar mascota: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la mascota"
        )


def get_vacunas_mascota(db: Session, mascota_id: int):
    """
    Obtener el registro de vacunas de una mascota
    """
    try:
        return db.query(VacunaDB).filter(
            VacunaDB.mascota_id == mascota_id
        ).order_by(VacunaDB.fecha.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener vacunas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener las vacunas"
        )



def create_vacuna(db: Session, mascota_id: int, vacuna: models.VacunaCreate):
    """
    Crear un nuevo registro de vacuna para una mascota
    """
    try:
        # Crear la instancia de VacunaDB, asegurando que mascota_id se pase correctamente
        db_vacuna = VacunaDB(
            mascota_id=mascota_id,  # Asegúrate de que esto esté presente
            **vacuna.dict()  # Esto incluirá todos los demás campos de vacuna
        )
        db.add(db_vacuna)
        db.commit()
        db.refresh(db_vacuna)
        return db_vacuna
    except SQLAlchemyError as e:
        logger.error(f"Error al crear registro de vacuna: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el registro de vacuna"
        )
def get_tratamientos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtener lista de tratamientos con paginación.
    """
    try:
        return db.query(TratamientoDB).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener tratamientos: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener la lista de tratamientos"
        )
def create_tratamiento(db: Session, tratamiento: models.TratamientoCreate) -> TratamientoDB:
    """
    Crear un nuevo tratamiento en la base de datos.
    
    Args:
        db (Session): La sesión de la base de datos.
        tratamiento (models.TratamientoCreate): Los datos del tratamiento a crear.

    Returns:
        TratamientoDB: El tratamiento creado.
    """
    try:
        # Crear una instancia de TratamientoDB a partir de los datos de TratamientoCreate
        db_tratamiento = TratamientoDB(**tratamiento.dict())
        
        # Agregar el tratamiento a la sesión de la base de datos
        db.add(db_tratamiento)
        db.commit()  # Confirmar los cambios
        db.refresh(db_tratamiento)  # Obtener el tratamiento creado con el ID generado
        
        logger.info(f"Tratamiento creado exitosamente: ID {db_tratamiento.id}")
        return db_tratamiento
    except SQLAlchemyError as e:
        logger.error(f"Error al crear tratamiento: {str(e)}")
        db.rollback()  # Deshacer cambios en caso de error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el tratamiento en la base de datos"
        )
def get_tratamiento(db: Session, tratamiento_id: int):
    """Obtener un tratamiento por su ID."""
    tratamiento = db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()
    if not tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

def update_tratamiento(db: Session, tratamiento_id: int, tratamiento: models.Tratamiento):
    """Modificar un tratamiento existente."""
    db_tratamiento = db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()
    if not db_tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    
    for key, value in tratamiento.dict(exclude_unset=True).items():
        setattr(db_tratamiento, key, value)

    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

def delete_tratamiento(db: Session, tratamiento_id: int):
    """Eliminar un tratamiento por su ID."""
    db_tratamiento = db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()
    if not db_tratamiento:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    
    db.delete(db_tratamiento)
    db.commit()
    return True
#joins

def get_citas_con_clientes(db: Session, skip: int = 0, limit: int = 100):
    """Obtener citas junto con la información del cliente asociado."""
    try:
        citas_con_clientes = (
            db.query(CitaDB, ClienteDB)
            .join(ClienteDB)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return citas_con_clientes
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener citas con clientes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a la base de datos"
        )
def aceptar_cita(db: Session, cita_id: int):
    """Cambiar el estado de la cita a 'confirmada'."""
    cita = db.query(CitaDB).filter(CitaDB.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    
    cita.estado = "confirmada"
    db.commit()
    db.refresh(cita)
    return cita

def completar_cita(db: Session, cita_id: int):
    """Cambiar el estado de la cita a 'completada' y crear una factura."""
    cita = db.query(CitaDB).filter(CitaDB.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Cambiar el estado de la cita a 'completada'
    cita.estado = "completada"
    db.commit()  # Asegúrate de confirmar los cambios en la cita
    db.refresh(cita)  # Refresca la cita para obtener los cambios

    # Crear la factura asociada
    if cita.tratamiento_id:
        tratamiento = db.query(TratamientoDB).filter(TratamientoDB.id == cita.tratamiento_id).first()
        if not tratamiento:
            raise HTTPException(status_code=404, detail="Tratamiento no encontrado")

        # Crear la factura
        db_factura = FacturaDB(cita_id=cita.id,cliente_id=cita.cliente_id,tratamiento_id=cita.tratamiento_id, precio=tratamiento.costo)
        db.add(db_factura)
        db.commit()  # Asegúrate de confirmar los cambios en la factura
        db.refresh(db_factura)  # Refresca la factura para obtener los cambios

    return cita  # Retornar la cita actualizada
def create_factura(db: Session, cita_id: int, precio: float) -> FacturaDB:
    """Crear una nueva factura para una cita."""
    db_factura = FacturaDB(cita_id=cita_id, precio=precio)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def get_facturas(db: Session, skip: int = 0, limit: int = 100) -> List[FacturaDB]:
    """Obtener una lista de facturas con paginación."""
    return db.query(FacturaDB).offset(skip).limit(limit).all()

def get_factura(db: Session, factura_id: int) -> FacturaDB:
    """Obtener una factura por su ID."""
    return db.query(FacturaDB).filter(FacturaDB.id == factura_id).first()
def cargar_veterinarios_iniciales(db: Session):
    """
    Cargar veterinarios iniciales en la base de datos.
    """
    veterinarios_iniciales = [
        {
            "nombre": "Javier",
            "apellido": "Maroto",
            "email": "javimaroto@example.com",
            "telefono": "8870082711767",
            "especialidad": "Cirugía General",
            "numero_colegiado": "COL123456",
            "horario_trabajo": "Lunes a Viernes, 8am a 6pm"
        },
        {
            "nombre": "Lucía",
            "apellido": "Fernández",
            "email": "lucia.fernandez@example.com",
            "telefono": "1234567890",
            "especialidad": "Dermatología Veterinaria",
            "numero_colegiado": "COL654321",
            "horario_trabajo": "Martes a Sábado, 9am a 5pm"
        },
        {
            "nombre": "Carlos",
            "apellido": "González",
            "email": "carlos.gonzalez@example.com",
            "telefono": "9876543210",
            "especialidad": "Medicina Interna",
            "numero_colegiado": "COL789012",
            "horario_trabajo": "Lunes, Miércoles y Viernes, 10am a 4pm"
        },
        {
            "nombre": "Ana",
            "apellido": "Pérez",
            "email": "ana.perez@example.com",
            "telefono": "1122334455",
            "especialidad": "Odontología Veterinaria",
            "numero_colegiado": "COL345678",
            "horario_trabajo": "Jueves y Viernes, 1pm a 7pm"
        }
    ]

    for veterinario in veterinarios_iniciales:
        # Verificar si ya existe un veterinario con el mismo email
        existing_veterinario = db.query(VeterinarioDB).filter(VeterinarioDB.email == veterinario["email"]).first()
        if not existing_veterinario:
            db_veterinario = VeterinarioDB(**veterinario)
            db.add(db_veterinario)

    db.commit()  # Confirmar los cambios