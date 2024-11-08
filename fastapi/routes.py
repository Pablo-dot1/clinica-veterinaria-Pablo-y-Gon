from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models
import models_db
import database

router = APIRouter()

# Función para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para Cliente
@router.post("/clientes/", response_model=models.Cliente)
def crear_cliente(cliente: models.Cliente, db: Session = Depends(get_db)):
    db_cliente = models_db.ClienteDB(
        nombre=cliente.nombre,
        telefono=cliente.telefono,
        direccion=cliente.direccion,
        email=cliente.email
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/", response_model=List[models.Cliente])
def obtener_clientes(db: Session = Depends(get_db)):
    return db.query(models_db.ClienteDB).all()

@router.get("/clientes/{cliente_id}", response_model=models.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models_db.ClienteDB).filter(models_db.ClienteDB.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# Rutas para Mascota
@router.post("/mascotas/", response_model=models.Mascota)
def crear_mascota(mascota: models.Mascota, db: Session = Depends(get_db)):
    db_mascota = models_db.MascotaDB(
        nombre=mascota.nombre,
        especie=mascota.especie,
        raza=mascota.raza,
        edad=mascota.edad,
        propietario_id=mascota.propietario_id
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/mascotas/", response_model=List[models.Mascota])
def obtener_mascotas(db: Session = Depends(get_db)):
    return db.query(models_db.MascotaDB).all()

@router.get("/mascotas/{mascota_id}", response_model=models.Mascota)
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    db_mascota = db.query(models_db.MascotaDB).filter(models_db.MascotaDB.id == mascota_id).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return db_mascota

# Rutas para Cita
@router.post("/citas/", response_model=models.Cita)
def crear_cita(cita: models.Cita, db: Session = Depends(get_db)):
    db_cita = models_db.CitaDB(
        fecha_hora=cita.fecha_hora,
        mascota_id=cita.mascota_id,
        motivo=cita.motivo
    )
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.get("/citas/", response_model=List[models.Cita])
def obtener_citas(db: Session = Depends(get_db)):
    return db.query(models_db.CitaDB).all()

@router.get("/citas/{cita_id}", response_model=models.Cita)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = db.query(models_db.CitaDB).filter(models_db.CitaDB.id == cita_id).first()
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return db_cita

# Rutas para Tratamiento
@router.post("/tratamientos/", response_model=models.Tratamiento)
def crear_tratamiento(tratamiento: models.Tratamiento, db: Session = Depends(get_db)):
    db_tratamiento = models_db.TratamientoDB(
        nombre=tratamiento.nombre,
        descripcion=tratamiento.descripcion,
        costo=tratamiento.costo
    )
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

@router.get("/tratamientos/", response_model=List[models.Tratamiento])
def obtener_tratamientos(db: Session = Depends(get_db)):
    return db.query(models_db.TratamientoDB).all()

@router.get("/tratamientos/{tratamiento_id}", response_model=models.Tratamiento)
def obtener_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    db_tratamiento = db.query(models_db.TratamientoDB).filter(models_db.TratamientoDB.id == tratamiento_id).first()
    if db_tratamiento is None:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return db_tratamiento

# Rutas para Producto
@router.post("/productos/", response_model=models.Producto)
def crear_producto(producto: models.Producto, db: Session = Depends(get_db)):
    db_producto = models_db.ProductoDB(
        codigo=producto.codigo,
        nombre=producto.nombre,
        cantidad=producto.cantidad,
        precio=producto.precio
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/productos/", response_model=List[models.Producto])
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(models_db.ProductoDB).all()
