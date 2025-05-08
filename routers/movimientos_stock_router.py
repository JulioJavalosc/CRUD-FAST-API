from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import MovimientosStock
from operations.movimientos_stock_operations import (
    create_movimiento_stock,
    get_movimiento_stock,
    get_movimientos_stock,
    update_movimiento_stock,
    delete_movimiento_stock,
)
from schemas.movimientos_stock import MovimientoStockCreate, MovimientoStockResponse, MovimientoStockUpdate
from database import get_db

router = APIRouter(prefix="/movimientos-stock", tags=["movimientos-stock"])


@router.get("/", response_model=List[MovimientoStockResponse])
def read_movimientos_stock(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_movimientos_stock(db, skip=skip, limit=limit)


@router.get("/{movimiento_id}", response_model=MovimientoStockResponse)
def read_movimiento_stock(movimiento_id: int, db: Session = Depends(get_db)):
    movimiento = get_movimiento_stock(db, movimiento_id=movimiento_id)
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento de stock not found")
    return movimiento


@router.post("/", response_model=MovimientoStockResponse)
def create_new_movimiento_stock(movimiento: MovimientoStockCreate, db: Session = Depends(get_db)):
    return create_movimiento_stock(db=db, movimiento=movimiento)


@router.put("/{movimiento_id}", response_model=MovimientoStockResponse)
def update_existing_movimiento_stock(movimiento_id: int, movimiento_data: MovimientoStockUpdate, db: Session = Depends(get_db)):
    db_movimiento = update_movimiento_stock(db, movimiento_id=movimiento_id, movimiento_data=movimiento_data)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento de stock not found")
    return db_movimiento


@router.delete("/{movimiento_id}")
def delete_movimiento_stock_route(movimiento_id: int, db: Session = Depends(get_db)):
    return delete_movimiento_stock(db, movimiento_id=movimiento_id)