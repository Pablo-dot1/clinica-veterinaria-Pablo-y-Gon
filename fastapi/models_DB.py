from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

# Modelo de Cliente en la base de datos
class ClienteDB(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String)
    direccion = Column(String, nullable=True)

    # Relación con Mascota
    mascotas = relationship("MascotaDB", back_populates="propietario")

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

# Modelo de Cita en la base de datos
class CitaDB(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime)
    mascota_id = Column(Integer, ForeignKey('mascotas.id'))
    motivo = Column(String)

    # Relación con Mascota
    mascota = relationship("MascotaDB")

# Modelo de Tratamiento en la base de datos
class TratamientoDB(Base):
    __tablename__ = 'tratamientos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    costo = Column(Float)
    cita_id = Column(Integer, ForeignKey('citas.id'))

    # Relación con Cita
    cita = relationship("CitaDB")
