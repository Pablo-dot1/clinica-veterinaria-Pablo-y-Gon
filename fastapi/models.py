from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
import re

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=50, strip_whitespace=True)
    apellido: str = Field(..., min_length=2, max_length=50, strip_whitespace=True)
    email: EmailStr
    telefono: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    direccion: str = Field(..., min_length=5, max_length=200, strip_whitespace=True)

    @validator('nombre', 'apellido')
    def validar_nombre(cls, v):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('Solo se permiten letras y espacios')
        return v.title()

    @validator('telefono')
    def validar_telefono(cls, v):
        v = v.replace(' ', '').replace('-', '')
        if not v.replace('+', '').isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return v

    class Config:
        from_attributes = True

class ClienteCreate(Cliente):
    class Config:
        from_attributes = True

class Veterinario(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=50, strip_whitespace=True)
    apellido: str = Field(..., min_length=2, max_length=50, strip_whitespace=True)
    email: EmailStr
    telefono: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    especialidad: str = Field(..., min_length=3, max_length=100, strip_whitespace=True)
    numero_colegiado: str = Field(..., min_length=4, max_length=20, strip_whitespace=True)
    horario_trabajo: str = Field(..., min_length=5, max_length=200)

class VeterinarioCreate(Veterinario):
    class Config:
        from_attributes = True

    @validator('numero_colegiado')
    def validar_numero_colegiado(cls, v):
        if not re.match(r'^[A-Z0-9-]+$', v.upper()):
            raise ValueError('Formato de número de colegiado inválido')
        return v.upper()

    class Config:
        from_attributes = True

class Mascota(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1, max_length=50, strip_whitespace=True)
    especie: str = Field(..., min_length=1, max_length=50)
    raza: str = Field(..., min_length=1, max_length=50)
    edad: int = Field(..., ge=0, le=50)
    peso: float = Field(..., gt=0, le=200)
    sexo: str = Field(..., pattern='^(M|H)$')
    cliente_id: int
    fecha_nacimiento: Optional[date] = None
    alergias: Optional[str] = None
    condiciones_especiales: Optional[str] = None

    @validator('fecha_nacimiento')
    def validar_fecha_nacimiento(cls, v):
        if v and v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser futura')
        return v

    @validator('peso')
    def validar_peso(cls, v):
        if not 0.1 <= v <= 200:
            raise ValueError('El peso debe estar entre 0.1 y 200 kg')
        return round(v, 2)

    class Config:
        from_attributes = True

class MascotaCreate(Mascota):
    class Config:
        from_attributes = True

class Vacuna(BaseModel):
    id: Optional[int] = None
    mascota_id: int
    nombre_vacuna: str = Field(..., min_length=2, max_length=100)
    fecha_aplicacion: datetime
    fecha_proxima: datetime
    veterinario_id: int
    lote: str = Field(..., min_length=4, max_length=50)
    notas: Optional[str] = None

class VacunaCreate(BaseModel):
    nombre_vacuna: str = Field(..., min_length=2, max_length=100)
    fecha_aplicacion: datetime
    fecha_proxima: datetime
    veterinario_id: int
    lote: str = Field(..., min_length=4, max_length=50)
    notas: Optional[str] = None

    class Config:
        from_attributes = True

    @validator('fecha_proxima')
    def validar_fecha_proxima(cls, v, values):
        if v and 'fecha_aplicacion' in values and v <= values['fecha_aplicacion']:
            raise ValueError('La fecha próxima debe ser posterior a la fecha de aplicación')
        return v

    @validator('lote')
    def validar_lote(cls, v):
        if not re.match(r'^[A-Z0-9-]+$', v.upper()):
            raise ValueError('Formato de lote inválido')
        return v.upper()

    class Config:
        from_attributes = True

class Cita(BaseModel):
    id: Optional[int] = None
    fecha: datetime
    motivo: str = Field(..., min_length=5, max_length=200)
    mascota_id: int
    veterinario_id: int
    cliente_id: int  # Agregado el atributo cliente_id
    estado: str = Field(..., pattern='^(pendiente|confirmada|cancelada|completada)$')
    notas: Optional[str] = None
    tratamiento_id: Optional[int] = None

    @validator('fecha')
    def validar_fecha_futura(cls, v):
        if v < datetime.now():
            raise ValueError('La fecha de la cita debe ser futura')
        return v

    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['pendiente', 'confirmada', 'cancelada', 'completada']
        if v not in estados_validos:
            raise ValueError(f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}')
        return v

    def puede_eliminar(self) -> bool:
        return self.estado != 'completada'

    class Config:
        from_attributes = True

class CitaCreate(BaseModel):
    fecha: datetime
    motivo: str = Field(..., min_length=5, max_length=200)
    mascota_id: int
    veterinario_id: int
    estado: str = Field(..., pattern='^(pendiente|confirmada|cancelada|completada)$')
    notas: Optional[str] = None
    tratamiento_id: Optional[int] = None
    cliente_id: int 

    @validator('fecha')
    def validar_fecha_futura(cls, v):
        if v < datetime.now():
            raise ValueError('La fecha de la cita debe ser futura')
        return v

    class Config:
        from_attributes = True

class CitaUpdate(BaseModel):
    fecha: Optional[datetime] = None
    motivo: Optional[str] = Field(None, min_length=5, max_length=200)
    estado: Optional[str] = Field(None, pattern='^(pendiente|confirmada|cancelada|completada)$')
    notas: Optional[str] = None
    tratamiento_id: Optional[int] = None

    @validator('fecha')
    def validar_fecha_futura(cls, v):
        if v and v < datetime.now():
            raise ValueError('La fecha de la cita debe ser futura')
        return v

    class Config:
        from_attributes = True

class Tratamiento(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=10, max_length=500)
    costo: float = Field(..., gt=0)
    duracion: Optional[int] = Field(None, ge=1)
    indicaciones: Optional[str] = None
    contraindicaciones: Optional[str] = None

    @validator('costo')
    def validar_costo(cls, v):
        if v <= 0:
            raise ValueError('El costo debe ser mayor que 0')
        return round(v, 2)

    @validator('duracion')
    def validar_duracion(cls, v):
        if v is not None and v < 1:
            raise ValueError('La duración debe ser al menos 1 día')
        return v

class TratamientoCreate(Tratamiento):
    class Config:
        from_attributes = True
        

class Medicamento(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=10, max_length=500)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    laboratorio: str = Field(..., min_length=2, max_length=100)
    principio_activo: str = Field(..., min_length=2, max_length=100)
    requiere_receta: bool
    fecha_caducidad: datetime

    @validator('fecha_caducidad')
    def validar_fecha_caducidad(cls, v):
        if v <= datetime.now():
            raise ValueError('La fecha de caducidad debe ser futura')
        return v

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que 0')
        return round(v, 2)

    class Config:
        from_attributes = True

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=10, max_length=500)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str = Field(..., max_length=50)
    proveedor: Optional[str] = None

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que 0')
        return round(v, 2)

    @validator('stock')
    def validar_stock(cls, v):
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

    class Config:
        from_attributes = True

class ProductoCreate(Producto):
    class Config:
        from_attributes = True

class Factura(BaseModel):
    id: Optional[int] = None
    cita_id: int
    precio: float
    cliente_id: int
    tratamiento_id: int
    fecha_emision: Optional[datetime] = None

    class Config:
        orm_mode = True