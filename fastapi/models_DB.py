from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Text, Enum
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class EstadoCita(enum.Enum):
    PROGRAMADA = "programada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

# Modelo de Cliente en la base de datos
class ClienteDB(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String, index=True)
    direccion = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)

    # Relaciones
    mascotas = relationship("MascotaDB", back_populates="propietario")
    reviews = relationship("ReviewDB", back_populates="cliente")
    facturas = relationship("FacturaDB", back_populates="cliente")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Mascota en la base de datos
class MascotaDB(Base):
    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    especie = Column(String)
    raza = Column(String)
    edad = Column(Integer)
    peso = Column(Float, nullable=True)
    propietario_id = Column(Integer, ForeignKey('clientes.id'))

    # Relaciones
    propietario = relationship("ClienteDB", back_populates="mascotas")
    citas = relationship("CitaDB", back_populates="mascota")
    historial_medico = relationship("HistorialMedicoDB", back_populates="mascota")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Cita en la base de datos
class CitaDB(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)
    veterinario_id = Column(Integer, ForeignKey('veterinarios.id'), nullable=False)
    motivo = Column(String, nullable=False)
    estado = Column(Enum(EstadoCita), default=EstadoCita.PROGRAMADA)
    notas = Column(Text, nullable=True)

    # Relaciones
    mascota = relationship("MascotaDB", back_populates="citas")
    veterinario = relationship("VeterinarioDB", back_populates="citas")
    tratamientos = relationship("TratamientoDB", back_populates="cita")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Tratamiento en la base de datos
class TratamientoDB(Base):
    __tablename__ = 'tratamientos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    costo = Column(Float, nullable=False)
    cita_id = Column(Integer, ForeignKey('citas.id'), nullable=False)
    medicamentos = Column(Text, nullable=True)
    instrucciones = Column(Text, nullable=True)

    # Relaciones
    cita = relationship("CitaDB", back_populates="tratamientos")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Producto en la base de datos
class ProductoDB(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=True)
    proveedor = Column(String(100), nullable=True)

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Review en la base de datos
class ReviewDB(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)

    # Relaciones
    cliente = relationship("ClienteDB", back_populates="reviews")

    fecha_creacion = Column(DateTime, default=func.now())

# Modelo de Veterinario en la base de datos
class VeterinarioDB(Base):
    __tablename__ = 'veterinarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    especialidad = Column(String, nullable=True)
    email = Column(String, unique=True)
    telefono = Column(String)

    # Relaciones
    citas = relationship("CitaDB", back_populates="veterinario")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())

# Modelo de Historial Médico en la base de datos
class HistorialMedicoDB(Base):
    __tablename__ = 'historial_medico'

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(Text, nullable=False)
    diagnostico = Column(Text, nullable=True)
    tratamiento = Column(Text, nullable=True)

    # Relaciones
    mascota = relationship("MascotaDB", back_populates="historial_medico")

    fecha_creacion = Column(DateTime, default=func.now())

# Modelo de Factura en la base de datos
class FacturaDB(Base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha = Column(DateTime, nullable=False, default=func.now())
    total = Column(Float, nullable=False)
    estado = Column(String, default='pendiente')
    detalles = Column(Text, nullable=True)

    # Relaciones
    cliente = relationship("ClienteDB", back_populates="facturas")

    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
