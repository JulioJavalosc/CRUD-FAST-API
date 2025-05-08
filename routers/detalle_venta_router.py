from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import DetalleVenta
from operations.detalle_venta_operations import (
    create_detalle_venta,
    get_detalle_venta,
    get_detalles_venta,
    update_detalle_venta,
    delete_detalle_venta,
)
from schemas.detalle_venta import DetalleVentaCreate, DetalleVentaResponse, DetalleVentaUpdate
from database import get_db

router = APIRouter(prefix="/detalles-venta", tags=["detalles-venta"])


@router.get("/", response_model=List[DetalleVentaResponse])
def read_detalles_venta(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_detalles_venta(db, skip=skip, limit=limit)


@router.get("/{detalle_id}", response_model=DetalleVentaResponse)
def read_detalle_venta(detalle_id: int, db: Session = Depends(get_db)):
    detalle = get_detalle_venta(db, detalle_id=detalle_id)
    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de venta not found")
    return detalle


@router.post("/", response_model=DetalleVentaResponse)
def create_new_detalle_venta(detalle: DetalleVentaCreate, db: Session = Depends(get_db)):
    return create_detalle_venta(db=db, detalle=detalle)


@router.put("/{detalle_id}", response_model=DetalleVentaResponse)
def update_existing_detalle_venta(detalle_id: int, detalle_data: DetalleVentaUpdate, db: Session = Depends(get_db)):
    db_detalle = update_detalle_venta(db, detalle_id=detalle_id, detalle_data=detalle_data)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de venta not found")
    return db_detalle


@router.delete("/{detalle_id}")
def delete_detalle_venta_route(detalle_id: int, db: Session = Depends(get_db)):
    return delete_detalle_venta(db, detalle_id=detalle_id)