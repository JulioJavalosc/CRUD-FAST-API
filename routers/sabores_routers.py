from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import SaboresBase
from operations.sabores_base_operations import (
    create_sabor_base,
    get_sabor_base,
    get_sabores_base,
    update_sabor_base,
    delete_sabor_base,
)
from schemas.sabores_base import SaborBaseCreate, SaborBaseResponse, SaborBaseUpdate
from database import get_db

router = APIRouter(prefix="/sabores-base", tags=["sabores-base"])


@router.get("/", response_model=List[SaborBaseResponse])
def read_sabores_base(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_sabores_base(db, skip=skip, limit=limit)


@router.get("/{sabor_id}", response_model=SaborBaseResponse)
def read_sabor_base(sabor_id: int, db: Session = Depends(get_db)):
    sabor = get_sabor_base(db, sabor_id=sabor_id)
    if sabor is None:
        raise HTTPException(status_code=404, detail="Sabor base not found")
    return sabor


@router.post("/", response_model=SaborBaseResponse)
def create_new_sabor_base(sabor: SaborBaseCreate, db: Session = Depends(get_db)):
    return create_sabor_base(db=db, sabor=sabor)


@router.put("/{sabor_id}", response_model=SaborBaseResponse)
def update_existing_sabor_base(sabor_id: int, sabor_data: SaborBaseUpdate, db: Session = Depends(get_db)):
    db_sabor = update_sabor_base(db, sabor_id=sabor_id, sabor_data=sabor_data)
    if db_sabor is None:
        raise HTTPException(status_code=404, detail="Sabor base not found")
    return db_sabor


@router.delete("/{sabor_id}")
def delete_sabor_base_route(sabor_id: int, db: Session = Depends(get_db)):
    return delete_sabor_base(db, sabor_id=sabor_id)