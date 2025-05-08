from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Ventas
from operations.ventas_operations import (
    create_venta,
    get_venta,
    get_ventas,
    update_venta,
    delete_venta,
    anular_venta,
)
from schemas.ventas import VentaCreate, VentaResponse, VentaUpdate
from database import get_db

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.get("/", response_model=List[VentaResponse])
def read_ventas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_ventas(db, skip=skip, limit=limit)


@router.get("/{venta_id}", response_model=VentaResponse)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = get_venta(db, venta_id=venta_id)
    if venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return venta


@router.post("/", response_model=VentaResponse)
def create_new_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    return create_venta(db=db, venta=venta)


@router.put("/{venta_id}", response_model=VentaResponse)
def update_existing_venta(venta_id: int, venta_data: VentaUpdate, db: Session = Depends(get_db)):
    db_venta = update_venta(db, venta_id=venta_id, venta_data=venta_data)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta not found")
    return db_venta


@router.delete("/{venta_id}")
def delete_venta_route(venta_id: int, db: Session = Depends(get_db)):
    return delete_venta(db, venta_id=venta_id)


@router.put("/anular/{venta_id}")
def anular_venta_route(venta_id: int, db: Session = Depends(get_db)):
    return anular_venta(db, venta_id=venta_id)