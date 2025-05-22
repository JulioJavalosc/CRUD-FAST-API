from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import ProductosFijos
from operations.productos_fijos_operations import (
    get_productos_fijos,
    get_producto_fijo,
    create_producto_fijo,
    update_producto_fijo,
    delete_producto_fijo,
    actualizar_stock_producto
)
from schemas.productos_fijos import ProductoFijoCreate, ProductoFijoUpdate, ProductoFijoResponse
from schemas.movimientos_stock import ActualizarStockRequest

router = APIRouter(prefix="/api/productos-fijos", tags=["Productos Fijos - REST"])

@router.get("/", response_model=List[ProductoFijoResponse])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_productos_fijos(db, skip=skip, limit=limit)

@router.get("/{producto_id}", response_model=ProductoFijoResponse)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = get_producto_fijo(db, producto_id=producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoFijoResponse)
def create_producto(producto: ProductoFijoCreate, db: Session = Depends(get_db)):
    return create_producto_fijo(db, producto=producto)

@router.put("/{producto_id}", response_model=ProductoFijoResponse)
def update_producto(producto_id: int, producto_data: ProductoFijoUpdate, db: Session = Depends(get_db)):
    db_producto = update_producto_fijo(db, producto_id=producto_id, producto_data=producto_data)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    resultado = delete_producto_fijo(db, producto_id=producto_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}

@router.put("/actualizar-stock/{producto_id}")
def actualizar_stock(
    producto_id: int,
    datos: ActualizarStockRequest,
    db: Session = Depends(get_db)
):
    return actualizar_stock_producto(db, producto_id=producto_id, nueva_cantidad=datos.nueva_cantidad, usuario_id=datos.usuario_id)