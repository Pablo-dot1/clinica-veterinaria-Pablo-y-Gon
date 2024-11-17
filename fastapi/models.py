from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, List
from datetime import datetime

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=2, max_length=50)
    apellido: constr(min_length=2, max_length=50)
    email: EmailStr
    telefono: str = Field(pattern=r'^\+?1?\d{9,15}$')
    direccion: constr(max_length=200)

    class Config:
        from_attributes = True

    @classmethod
    def telefono_valido(cls, v):
        if not v.replace('+', '').replace('-', '').isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return v

class Veterinario(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=2, max_length=50)
    apellido: constr(min_length=2, max_length=50)
    email: EmailStr
    telefono: str = Field(pattern=r'^\+?1?\d{9,15}$')
    especialidad: constr(max_length=100)
    numero_colegiado: constr(max_length=20)
    horario_trabajo: constr(max_length=200)

    class Config:
        from_attributes = True

class Mascota(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=1, max_length=50)
    especie: constr(min_length=1, max_length=50)
    raza: constr(min_length=1, max_length=50)
    edad: int
    peso: float
    sexo: str = Field(pattern='^(M|H)$')
    cliente_id: int
    fecha_nacimiento: Optional[datetime] = None
    alergias: Optional[str] = None
    condiciones_especiales: Optional[str] = None

    @classmethod
    def edad_valida(cls, v):
        if v < 0 or v > 50:
            raise ValueError('La edad debe estar entre 0 y 50 años')
        return v

    @classmethod
    def peso_valido(cls, v):
        if v <= 0:
            raise ValueError('El peso debe ser mayor que 0')
        return v

    class Config:
        from_attributes = True

class HistorialMedico(BaseModel):
    id: Optional[int] = None
    mascota_id: int
    fecha: datetime
    diagnostico: constr(min_length=10, max_length=500)
    tratamiento: constr(min_length=10, max_length=500)
    notas: Optional[str] = None
    veterinario_id: int
    proxima_revision: Optional[datetime] = None

    class Config:
        from_attributes = True

class Vacuna(BaseModel):
    id: Optional[int] = None
    mascota_id: int
    nombre_vacuna: constr(min_length=2, max_length=100)
    fecha_aplicacion: datetime
    fecha_proxima: datetime
    veterinario_id: int
    lote: constr(max_length=50)
    notas: Optional[str] = None

    class Config:
        from_attributes = True

class Cita(BaseModel):
    id: Optional[int] = None
    fecha: datetime
    motivo: constr(min_length=5, max_length=200)
    mascota_id: int
    veterinario_id: int
    estado: str = Field(pattern='^(pendiente|confirmada|cancelada|completada)$')
    notas: Optional[str] = None
    tratamiento_id: Optional[int] = None

    @classmethod
    def fecha_futura(cls, v):
        if v < datetime.now():
            raise ValueError('La fecha de la cita debe ser futura')
        return v

    class Config:
        from_attributes = True

class Tratamiento(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=2, max_length=100)
    descripcion: constr(min_length=10, max_length=500)
    costo: float
    duracion: Optional[int] = None  # duración en días
    indicaciones: Optional[str] = None
    contraindicaciones: Optional[str] = None

    @classmethod
    def costo_positivo(cls, v):
        if v <= 0:
            raise ValueError('El costo debe ser mayor que 0')
        return v

    class Config:
        from_attributes = True

class Medicamento(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=2, max_length=100)
    descripcion: constr(min_length=10, max_length=500)
    precio: float
    stock: int
    laboratorio: str
    principio_activo: str
    requiere_receta: bool
    fecha_caducidad: datetime

    @classmethod
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que 0')
        return v

    @classmethod
    def stock_positivo(cls, v):
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

    class Config:
        from_attributes = True

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: constr(min_length=2, max_length=100)
    descripcion: constr(min_length=10, max_length=500)
    precio: float
    stock: int
    categoria: constr(max_length=50)
    proveedor: Optional[str] = None

    @classmethod
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que 0')
        return v

    @classmethod
    def stock_positivo(cls, v):
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

    class Config:
        from_attributes = True

class Factura(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    fecha: datetime = datetime.now()
    total: float
    estado: str = Field(pattern='^(pendiente|pagada|cancelada)$')
    metodo_pago: str = Field(pattern='^(efectivo|tarjeta|transferencia)$')
    items: List[dict]  # Lista de productos/servicios facturados

    @classmethod
    def total_positivo(cls, v):
        if v <= 0:
            raise ValueError('El total debe ser mayor que 0')
        return v

    class Config:
        from_attributes = True

class Review(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    calificacion: int
    comentario: constr(min_length=10, max_length=500)
    fecha: datetime = datetime.now()
    veterinario_id: Optional[int] = None
    servicio_evaluado: Optional[str] = None

    @classmethod
    def calificacion_valida(cls, v):
        if v < 1 or v > 5:
            raise ValueError('La calificación debe estar entre 1 y 5')
        return v

    class Config:
        from_attributes = True
