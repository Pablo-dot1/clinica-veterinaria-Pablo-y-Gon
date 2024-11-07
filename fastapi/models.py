from pydantic import BaseModel, Field, root_validator
from typing import Optional
from datetime import datetime

class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')  # Validación para un teléfono internacional
    direccion: Optional[str] = None
    # Añadir validación personalizada si es necesario (por ejemplo, si el cliente debe tener al menos una mascota)
    @root_validator
    def check_cliente(cls, values):
        # Implementar validaciones de cliente si es necesario
        return values

class Mascota(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int = Field(..., ge=0)  # Edad debe ser mayor o igual a 0
    propietario_id: int

class Cita(BaseModel):
    id: int
    fecha_hora: datetime
    mascota_id: int
    motivo: str

class Tratamiento(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None  # Hacer descripción opcional
    costo: float = Field(..., gt=0)  # Costo debe ser mayor que 0

    @root_validator
    def check_tratamiento(cls, values):
        if values.get('costo') <= 0:
            raise ValueError('El costo debe ser mayor a 0')
        return values

class Producto(BaseModel):
    codigo: str
    nombre: str
    cantidad: int
    precio: float
