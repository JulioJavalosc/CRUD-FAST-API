from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import ProductosFijos
from operations.productos_fijos_operations import (
    create_producto_fijo,
    get_producto_fijo,
    get_productos_fijos,
    update_producto_fijo,
    delete_producto_fijo,
    actualizar_stock_producto
)
from schemas.movimientos_stock import ActualizarStockRequest
from schemas.productos_fijos import ProductoFijoCreate, ProductoFijoResponse, ProductoFijoUpdate
from database import get_db

router = APIRouter(prefix="/productos-fijos", tags=["productos-fijos"])


@router.get("/", response_model=List[ProductoFijoResponse])
def read_productos_fijos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_productos_fijos(db, skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoFijoResponse)
def read_producto_fijo(producto_id: int, db: Session = Depends(get_db)):
    producto = get_producto_fijo(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto fijo not found")
    return producto


@router.post("/", response_model=ProductoFijoResponse)
def create_new_producto_fijo(producto: ProductoFijoCreate, db: Session = Depends(get_db)):
    return create_producto_fijo(db=db, producto=producto)


@router.put("/{producto_id}", response_model=ProductoFijoResponse)
def update_existing_producto_fijo(producto_id: int, producto_data: ProductoFijoUpdate, db: Session = Depends(get_db)):
    db_producto = update_producto_fijo(db, producto_id=producto_id, producto_data=producto_data)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto fijo not found")
    return db_producto


@router.delete("/{producto_id}")
def delete_producto_fijo_route(producto_id: int, db: Session = Depends(get_db)):
    return delete_producto_fijo(db, producto_id=producto_id)

@router.put("/actualizar-stock/{producto_id}")
def actualizar_stock(
    producto_id: int,
    datos: ActualizarStockRequest,  # Datos del cuerpo de la solicitud
    db: Session = Depends(get_db)
):
    # Extraer los datos del cuerpo
    nueva_cantidad = datos.nueva_cantidad
    usuario_id = datos.usuario_id
    print("PRODUCTO",producto_id)
    print("USUARIO",usuario_id)
    print("NUEVA CANTIDAD",nueva_cantidad)
    # Llamar a la función que actualiza el stock y registra el movimiento
    return actualizar_stock_producto(db, producto_id, nueva_cantidad, usuario_id)