# __init__.py
from .database import engine, SessionLocal
from .models_db import ClienteDB, MascotaDB, CitaDB, TratamientoDB, ProductoDB
from .models import Cliente, Mascota, Cita, Tratamiento, Producto
from .routes import router
