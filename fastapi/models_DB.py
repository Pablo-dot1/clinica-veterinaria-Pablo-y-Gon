from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

# Modelo de Cliente en la base de datos
class ClienteDB(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String, index=True)
    direccion = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)  # Email único para cada cliente

    # Relación con Mascota
    mascotas = relationship("MascotaDB", back_populates="propietario")

    # Para registrar la fecha de creación del cliente
    fecha_creacion = Column(DateTime, default=func.now())

# Modelo de Mascota en la base de datos
class MascotaDB(Base):
    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    especie = Column(String)
    raza = Column(String)
    edad = Column(Integer)
    propietario_id = Column(Integer, ForeignKey('clientes.id'))

    # Relación con Cliente
    propietario = relationship("ClienteDB", back_populates="mascotas")

    # Para registrar la fecha de creación de la mascota
    fecha_creacion = Column(DateTime, default=func.now())

# Modelo de Cita en la base de datos
class CitaDB(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)
    motivo = Column(String, nullable=False)

    # Relación con Mascota
    mascota = relationship("MascotaDB")

    # Para registrar la fecha de creación de la cita
    fecha_creacion = Column(DateTime, default=func.now())

# Modelo de Tratamiento en la base de datos
class TratamientoDB(Base):
    __tablename__ = 'tratamientos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    costo = Column(Float, nullable=False)
    cita_id = Column(Integer, ForeignKey('citas.id'), nullable=False)

    # Relación con Cita
    cita = relationship("CitaDB", backref="tratamientos")

    # Para registrar la fecha de creación del tratamiento
    fecha_creacion = Column(DateTime, default=func.now())

class ProductoDB(Base):
    __tablename__ = 'productos'

    IDPRODUCTO = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True)
    nombre = Column(String(100))
    cantidad = Column(Integer)
    precio = Column(Float)
