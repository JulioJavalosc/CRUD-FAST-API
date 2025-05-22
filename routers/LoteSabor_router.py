from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from models import LotesSaboresBase
from schemas.LoteSabor import LoteSaborCreate, LoteSabor
from operations.LoteSabor_operations import (
    get_lote,
    create_lote,
    update_lote,
    delete_lote
)
from database import get_db

router = APIRouter(prefix="/api/lotes", tags=["Lotes - API"])

@router.get("/", response_model=list[LoteSabor])
def read_lotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_lote(db, skip=skip, limit=limit)

@router.post("/", response_model=LoteSabor)
def create_new_lote(lote: LoteSaborCreate, db: Session = Depends(get_db)):
    return create_lote(db=db, lote=lote)

@router.get("/{lote_id}", response_model=LoteSabor)
def read_detalle_lote(lote_id: int, db: Session = Depends(get_db)):
    db_lote = get_lote(db, lote_id=lote_id)
    if not db_lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return db_lote

@router.put("/{lote_id}", response_model=LoteSabor)
def update_existing_lote(lote_id: int, lote: LoteSaborCreate, db: Session = Depends(get_db)):
    db_lote = update_lote(db, lote_id=lote_id, lote_data=lote)
    if not db_lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return db_lote

@router.delete("/{lote_id}")
def delete_existing_lote(lote_id: int, db: Session = Depends(get_db)):
    resultado = delete_lote(db, lote_id=lote_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return {"message": "Lote eliminado"}