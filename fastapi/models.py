from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str
    direccion: Optional[str] = None

class Mascota(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int
    propietario_id: int
class Cita(BaseModel):
    id: int
    fecha_hora: datetime
    mascota_id: int
    motivo: str

class Tratamiento(BaseModel):
    id: int
    nombre: str
    descripcion: str
    costo: float
