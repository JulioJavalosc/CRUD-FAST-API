from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import HeladosPersonalizados
from operations.helados_personalizados_operations import (
    create_helado_personalizado,
    get_helado_personalizado,
    get_helados_personalizados,
    update_helado_personalizado,
    delete_helado_personalizado,
)
from schemas.helados_personalizados import HeladoPersonalizadoCreate, HeladoPersonalizadoResponse, HeladoPersonalizadoUpdate
from database import get_db

router = APIRouter(prefix="/helados-personalizados", tags=["helados-personalizados"])


@router.get("/", response_model=List[HeladoPersonalizadoResponse])
def read_helados_personalizados(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_helados_personalizados(db, skip=skip, limit=limit)


@router.get("/{helado_id}", response_model=HeladoPersonalizadoResponse)
def read_helado_personalizado(helado_id: int, db: Session = Depends(get_db)):
    helado = get_helado_personalizado(db, helado_id=helado_id)
    if helado is None:
        raise HTTPException(status_code=404, detail="Helado personalizado not found")
    return helado


@router.post("/", response_model=HeladoPersonalizadoResponse)
def create_new_helado_personalizado(helado: HeladoPersonalizadoCreate, db: Session = Depends(get_db)):
    return create_helado_personalizado(db=db, helado=helado)


@router.put("/{helado_id}", response_model=HeladoPersonalizadoResponse)
def update_existing_helado_personalizado(helado_id: int, helado_data: HeladoPersonalizadoUpdate, db: Session = Depends(get_db)):
    db_helado = update_helado_personalizado(db, helado_id=helado_id, helado_data=helado_data)
    if db_helado is None:
        raise HTTPException(status_code=404, detail="Helado personalizado not found")
    return db_helado


@router.delete("/{helado_id}")
def delete_helado_personalizado_route(helado_id: int, db: Session = Depends(get_db)):
    return delete_helado_personalizado(db, helado_id=helado_id)