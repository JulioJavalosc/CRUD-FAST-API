from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import DetalleHeladoPersonalizado
from operations.detalle_helado_personalizado_operations import (
    create_detalle_helado_personalizado,
    get_detalle_helado_personalizado,
    get_detalles_helado_personalizado,
    update_detalle_helado_personalizado,
    delete_detalle_helado_personalizado,
)
from schemas.detalle_helado_personalizado import DetalleHeladoPersonalizadoCreate, DetalleHeladoPersonalizadoResponse, DetalleHeladoPersonalizadoUpdate
from database import get_db

router = APIRouter(prefix="/detalles-helado-personalizado", tags=["detalles-helado-personalizado"])


@router.get("/", response_model=List[DetalleHeladoPersonalizadoResponse])
def read_detalles_helado_personalizado(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_detalles_helado_personalizado(db, skip=skip, limit=limit)


@router.get("/{detalle_id}", response_model=DetalleHeladoPersonalizadoResponse)
def read_detalle_helado_personalizado(detalle_id: int, db: Session = Depends(get_db)):
    detalle = get_detalle_helado_personalizado(db, detalle_id=detalle_id)
    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de helado personalizado not found")
    return detalle


@router.post("/", response_model=DetalleHeladoPersonalizadoResponse)
def create_new_detalle_helado_personalizado(detalle: DetalleHeladoPersonalizadoCreate, db: Session = Depends(get_db)):
    return create_detalle_helado_personalizado(db=db, detalle=detalle)


@router.put("/{detalle_id}", response_model=DetalleHeladoPersonalizadoResponse)
def update_existing_detalle_helado_personalizado(detalle_id: int, detalle_data: DetalleHeladoPersonalizadoUpdate, db: Session = Depends(get_db)):
    db_detalle = update_detalle_helado_personalizado(db, detalle_id=detalle_id, detalle_data=detalle_data)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle de helado personalizado not found")
    return db_detalle


@router.delete("/{detalle_id}")
def delete_detalle_helado_personalizado_route(detalle_id: int, db: Session = Depends(get_db)):
    return delete_detalle_helado_personalizado(db, detalle_id=detalle_id)