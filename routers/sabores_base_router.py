from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import SaboresBase
from schemas.sabores_base import SaborBaseCreate, SaborBaseResponse, SaborBaseUpdate
from operations.sabores_base_operations import (
    get_sabores_base,
    get_sabor_base,
    create_sabor_base as op_create,
    update_sabor_base as op_update,
    delete_sabor_base as op_delete
)
router = APIRouter(prefix="/api/sabores-base", tags=["Sabores Base - API"])
@router.get("/", response_model=list[SaborBaseResponse])
def read_sabores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_sabores_base(db, skip=skip, limit=limit)
@router.get("/{sabor_id}", response_model=SaborBaseResponse)
def read_sabor(sabor_id: int, db: Session = Depends(get_db)):
    sabor = get_sabor_base(db, sabor_id=sabor_id)
    if not sabor:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return sabor
@router.post("/", response_model=SaborBaseResponse)
def create_new_sabor(sabor: SaborBaseCreate, db: Session = Depends(get_db)):
    return op_create(db=db, sabor=sabor)
@router.put("/{sabor_id}", response_model=SaborBaseResponse)
def update_existing_sabor(sabor_id: int, sabor_data: SaborBaseUpdate, db: Session = Depends(get_db)):
    db_sabor = op_update(db, sabor_id=sabor_id, sabor_data=sabor_data)
    if not db_sabor:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return db_sabor
@router.delete("/{sabor_id}")
def delete_existing_sabor(sabor_id: int, db: Session = Depends(get_db)):
    resultado = op_delete(db, sabor_id=sabor_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return {"message": "Sabor eliminado correctamente"}