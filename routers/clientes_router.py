from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Clientes
from operations.clientes_operations import (
    create_cliente,
    get_cliente,
    get_clientes,
    update_cliente,
    delete_cliente,
)
from schemas.clientes import ClienteCreate, ClienteResponse, ClienteUpdate
from database import get_db

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteResponse])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_clientes(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = get_cliente(db, cliente_id=cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente


@router.post("/", response_model=ClienteResponse)
def create_new_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db=db, cliente=cliente)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_existing_cliente(cliente_id: int, cliente_data: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = update_cliente(db, cliente_id=cliente_id, cliente_data=cliente_data)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente


@router.delete("/{cliente_id}")
def delete_cliente_route(cliente_id: int, db: Session = Depends(get_db)):
    return delete_cliente(db, cliente_id=cliente_id)