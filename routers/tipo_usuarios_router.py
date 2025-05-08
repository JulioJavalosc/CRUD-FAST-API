from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import TipoUsuarios
from operations.tipo_usuarios_operations import (
    create_tipo_usuario,
    get_tipo_usuario,
    get_tipo_usuarios,
    update_tipo_usuario,
    delete_tipo_usuario,
)
from schemas.tipo_usuarios import TipoUsuarioCreate, TipoUsuarioResponse, TipoUsuarioUpdate
from database import get_db

router = APIRouter(prefix="/tipo-usuarios", tags=["tipo-usuarios"])


@router.get("/", response_model=List[TipoUsuarioResponse])
def read_tipo_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tipo_usuarios(db, skip=skip, limit=limit)


@router.get("/{tipo_usuario_id}", response_model=TipoUsuarioResponse)
def read_tipo_usuario(tipo_usuario_id: int, db: Session = Depends(get_db)):
    tipo_usuario = get_tipo_usuario(db, tipo_usuario_id=tipo_usuario_id)
    if tipo_usuario is None:
        raise HTTPException(status_code=404, detail="Tipo de usuario not found")
    return tipo_usuario


@router.post("/", response_model=TipoUsuarioResponse)
def create_new_tipo_usuario(tipo_usuario: TipoUsuarioCreate, db: Session = Depends(get_db)):
    return create_tipo_usuario(db=db, tipo_usuario=tipo_usuario)


@router.put("/{tipo_usuario_id}", response_model=TipoUsuarioResponse)
def update_existing_tipo_usuario(tipo_usuario_id: int, tipo_usuario_data: TipoUsuarioUpdate, db: Session = Depends(get_db)):
    db_tipo_usuario = update_tipo_usuario(db, tipo_usuario_id=tipo_usuario_id, tipo_usuario_data=tipo_usuario_data)
    if db_tipo_usuario is None:
        raise HTTPException(status_code=404, detail="Tipo de usuario not found")
    return db_tipo_usuario


@router.delete("/{tipo_usuario_id}")
def delete_tipo_usuario_route(tipo_usuario_id: int, db: Session = Depends(get_db)):
    return delete_tipo_usuario(db, tipo_usuario_id=tipo_usuario_id)