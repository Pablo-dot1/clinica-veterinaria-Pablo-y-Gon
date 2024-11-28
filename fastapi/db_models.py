from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ClienteDB(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    telefono = Column(String(15))
    direccion = Column(String(200))

    mascotas = relationship("MascotaDB", back_populates="cliente")

class VeterinarioDB(Base):
    __tablename__ = "veterinarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    telefono = Column(String(15))
    especialidad = Column(String(100))
    numero_colegiado = Column(String(20))
    horario_trabajo = Column(String(200))

class MascotaDB(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    especie = Column(String(50))
    raza = Column(String(50))
    edad = Column(Integer)
    peso = Column(Float)
    sexo = Column(String(1))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha_nacimiento = Column(DateTime, nullable=True)
    alergias = Column(String, nullable=True)
    condiciones_especiales = Column(String, nullable=True)

    cliente = relationship("ClienteDB", back_populates="mascotas")
    historial_medico = relationship("HistorialMedicoDB", back_populates="mascota")
    vacunas = relationship("VacunaDB", back_populates="mascota")

class HistorialMedicoDB(Base):
    __tablename__ = "historial_medico"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    fecha = Column(DateTime)
    diagnostico = Column(String(500))
    tratamiento = Column(String(500))
    notas = Column(String, nullable=True)
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))
    proxima_revision = Column(DateTime, nullable=True)

    mascota = relationship("MascotaDB", back_populates="historial_medico")

class VacunaDB(Base):
    __tablename__ = "vacunas"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    nombre_vacuna = Column(String(100))
    fecha_aplicacion = Column(DateTime)
    fecha_proxima = Column(DateTime)
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))
    lote = Column(String(50))
    notas = Column(String, nullable=True)

    mascota = relationship("MascotaDB", back_populates="vacunas")

class CitaDB(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    motivo = Column(String(200))
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    veterinario_id = Column(Integer, ForeignKey("veterinarios.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    estado = Column(String(20))
    notas = Column(String, nullable=True)
    tratamiento_id = Column(Integer, ForeignKey("tratamientos.id"), nullable=True)
    factura = relationship("FacturaDB", back_populates="cita", uselist=False)
class TratamientoDB(Base):
    __tablename__ = "tratamientos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(500))
    costo = Column(Float)
    duracion = Column(Integer, nullable=True)
    indicaciones = Column(String, nullable=True)
    contraindicaciones = Column(String, nullable=True)



class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(500))
    precio = Column(Float)
    stock = Column(Integer)
    categoria = Column(String(50))
    proveedor = Column(String(100), nullable=True)


class FacturaDB(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("citas.id"))
    precio = Column(Float)
    fecha_emision = Column(DateTime, default=datetime.utcnow)

    cita = relationship("CitaDB", back_populates="factura")
