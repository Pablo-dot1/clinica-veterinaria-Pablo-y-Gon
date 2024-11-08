from pydantic import BaseModel, Field, root_validator
from typing import Optional
from datetime import datetime

class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')  # Validación para un teléfono internacional
    direccion: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True

class Mascota(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int = Field(..., ge=0)
    propietario_id: int

    class Config:
        orm_mode = True

class Cita(BaseModel):
    id: int
    fecha_hora: datetime
    mascota_id: int
    motivo: str

    class Config:
        orm_mode = True

class Tratamiento(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    costo: float = Field(..., gt=0)

    class Config:
        orm_mode = True

class Producto(BaseModel):
    codigo: str
    nombre: str
    cantidad: int
    precio: float

    class Config:
        orm_mode = True
