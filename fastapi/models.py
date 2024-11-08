from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')  # Se usa 'pattern' en lugar de 'regex'
    direccion: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True

class Mascota(BaseModel):
    id: Optional[int] = None  # El 'id' puede ser None al crear un objeto
    nombre: str
    especie: str
    raza: str
    edad: int = Field(..., ge=0)  # La edad debe ser >= 0
    propietario_id: int

    class Config:
        orm_mode = True

class Cita(BaseModel):
    id: Optional[int] = None  # El 'id' puede ser None al crear un objeto
    fecha_hora: datetime
    mascota_id: int
    motivo: str

    class Config:
        orm_mode = True

class Tratamiento(BaseModel):
    id: Optional[int] = None  # El 'id' puede ser None al crear un objeto
    nombre: str
    descripcion: Optional[str] = None
    costo: float = Field(..., gt=0)  # El costo debe ser mayor que 0

    class Config:
        orm_mode = True

class Producto(BaseModel):
    codigo: str
    nombre: str
    cantidad: int = Field(..., ge=0)  # La cantidad debe ser >= 0
    precio: float = Field(..., gt=0)  # El precio debe ser mayor que 0

    class Config:
        orm_mode = True
