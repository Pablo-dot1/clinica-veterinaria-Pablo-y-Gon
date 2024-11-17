from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models
import crud
from database import get_db
from fastapi import status

router = APIRouter(
    tags=["Clínica Veterinaria"],
    responses={404: {"description": "No encontrado"}},
)

# Cliente endpoints
@router.post("/clientes/", response_model=models.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: models.Cliente, db: Session = Depends(get_db)):
    """Crear un nuevo cliente"""
    try:
        return crud.create_cliente(db=db, cliente=cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes/", response_model=List[models.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todos los clientes"""
    try:
        clientes = crud.get_clientes(db, skip=skip, limit=limit)
        return clientes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes/{cliente_id}", response_model=models.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener un cliente específico"""
    try:
        cliente = crud.get_cliente(db, cliente_id=cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/clientes/{cliente_id}", response_model=models.Cliente)
def update_cliente(cliente_id: int, cliente: models.Cliente, db: Session = Depends(get_db)):
    """Actualizar un cliente"""
    try:
        updated_cliente = crud.update_cliente(db, cliente_id, cliente)
        if updated_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return updated_cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Eliminar un cliente"""
    try:
        success = crud.delete_cliente(db, cliente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"message": "Cliente eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mascota endpoints
@router.post("/mascotas/", response_model=models.Mascota, status_code=status.HTTP_201_CREATED)
def create_mascota(mascota: models.Mascota, db: Session = Depends(get_db)):
    """Crear una nueva mascota"""
    try:
        return crud.create_mascota(db=db, mascota=mascota)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/mascotas/", response_model=List[models.Mascota])
def read_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las mascotas"""
    try:
        mascotas = crud.get_mascotas(db, skip=skip, limit=limit)
        return mascotas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/mascotas/{mascota_id}", response_model=models.Mascota)
def read_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """Obtener una mascota específica"""
    try:
        mascota = crud.get_mascota(db, mascota_id)
        if mascota is None:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return mascota
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/mascotas/{mascota_id}", response_model=models.Mascota)
def update_mascota(mascota_id: int, mascota: models.Mascota, db: Session = Depends(get_db)):
    """Actualizar una mascota"""
    try:
        updated_mascota = crud.update_mascota(db, mascota_id, mascota)
        if updated_mascota is None:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return updated_mascota
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/mascotas/{mascota_id}")
def delete_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """Eliminar una mascota"""
    try:
        success = crud.delete_mascota(db, mascota_id)
        if not success:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        return {"message": "Mascota eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Cita endpoints
@router.post("/citas/", response_model=models.Cita, status_code=status.HTTP_201_CREATED)
def create_cita(cita: models.Cita, db: Session = Depends(get_db)):
    """Crear una nueva cita"""
    try:
        return crud.create_cita(db=db, cita=cita)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/citas/", response_model=List[models.Cita])
def read_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las citas"""
    try:
        citas = crud.get_citas(db, skip=skip, limit=limit)
        return citas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/citas/{cita_id}", response_model=models.Cita)
def read_cita(cita_id: int, db: Session = Depends(get_db)):
    """Obtener una cita específica"""
    try:
        cita = crud.get_cita(db, cita_id)
        if cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return cita
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/citas/{cita_id}", response_model=models.Cita)
def update_cita(cita_id: int, cita: models.Cita, db: Session = Depends(get_db)):
    """Actualizar una cita"""
    try:
        updated_cita = crud.update_cita(db, cita_id, cita)
        if updated_cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return updated_cita
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/citas/{cita_id}")
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    """Eliminar una cita"""
    try:
        success = crud.delete_cita(db, cita_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return {"message": "Cita eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Tratamiento endpoints
@router.post("/tratamientos/", response_model=models.Tratamiento, status_code=status.HTTP_201_CREATED)
def create_tratamiento(tratamiento: models.Tratamiento, db: Session = Depends(get_db)):
    """Crear un nuevo tratamiento"""
    try:
        return crud.create_tratamiento(db=db, tratamiento=tratamiento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tratamientos/", response_model=List[models.Tratamiento])
def read_tratamientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todos los tratamientos"""
    try:
        tratamientos = crud.get_tratamientos(db, skip=skip, limit=limit)
        return tratamientos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tratamientos/{tratamiento_id}", response_model=models.Tratamiento)
def read_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    """Obtener un tratamiento específico"""
    try:
        tratamiento = crud.get_tratamiento(db, tratamiento_id)
        if tratamiento is None:
            raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
        return tratamiento
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tratamientos/{tratamiento_id}", response_model=models.Tratamiento)
def update_tratamiento(tratamiento_id: int, tratamiento: models.Tratamiento, db: Session = Depends(get_db)):
    """Actualizar un tratamiento"""
    try:
        updated_tratamiento = crud.update_tratamiento(db, tratamiento_id, tratamiento)
        if updated_tratamiento is None:
            raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
        return updated_tratamiento
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tratamientos/{tratamiento_id}")
def delete_tratamiento(tratamiento_id: int, db: Session = Depends(get_db)):
    """Eliminar un tratamiento"""
    try:
        success = crud.delete_tratamiento(db, tratamiento_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
        return {"message": "Tratamiento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Producto endpoints
@router.post("/productos/", response_model=models.Producto, status_code=status.HTTP_201_CREATED)
def create_producto(producto: models.Producto, db: Session = Depends(get_db)):
    """Crear un nuevo producto"""
    try:
        return crud.create_producto(db=db, producto=producto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/productos/", response_model=List[models.Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todos los productos"""
    try:
        productos = crud.get_productos(db, skip=skip, limit=limit)
        return productos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/productos/{producto_id}", response_model=models.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto específico"""
    try:
        producto = crud.get_producto(db, producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/productos/{producto_id}", response_model=models.Producto)
def update_producto(producto_id: int, producto: models.Producto, db: Session = Depends(get_db)):
    """Actualizar un producto"""
    try:
        updated_producto = crud.update_producto(db, producto_id, producto)
        if updated_producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return updated_producto
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto"""
    try:
        success = crud.delete_producto(db, producto_id)
        if not success:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"message": "Producto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Review endpoints
@router.post("/reviews/", response_model=models.Review, status_code=status.HTTP_201_CREATED)
def create_review(review: models.Review, db: Session = Depends(get_db)):
    """Crear una nueva review"""
    try:
        return crud.create_review(db=db, review=review)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reviews/", response_model=List[models.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las reviews"""
    try:
        reviews = crud.get_reviews(db, skip=skip, limit=limit)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reviews/{review_id}", response_model=models.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    """Obtener una review específica"""
    try:
        review = crud.get_review(db, review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Review no encontrada")
        return review
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/reviews/{review_id}", response_model=models.Review)
def update_review(review_id: int, review: models.Review, db: Session = Depends(get_db)):
    """Actualizar una review"""
    try:
        updated_review = crud.update_review(db, review_id, review)
        if updated_review is None:
            raise HTTPException(status_code=404, detail="Review no encontrada")
        return updated_review
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Eliminar una review"""
    try:
        success = crud.delete_review(db, review_id)
        if not success:
            raise HTTPException(status_code=404, detail="Review no encontrada")
        return {"message": "Review eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
