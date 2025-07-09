from datetime import datetime, timedelta
import secrets
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from models import Usuarios
from operations.usuarios_operations import (
    get_usuarios,
    get_usuario,
    create_usuario,
    update_usuario,
    delete_usuario,
    validate_usuario,
)
from schemas.user import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioValidate
from database import get_db

router = APIRouter(prefix="/usuariosa", tags=["usuarios"])
def verificar_contraseña(contraseña_plana: str, contraseña_hasheada: str) -> bool:
    return bcrypt.checkpw(contraseña_plana.encode('utf-8'), contraseña_hasheada.encode('utf-8'))


@router.get("/", response_model=List[UsuarioResponse])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db, skip=skip, limit=limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario


@router.post("/validate/")
def validate_usuario_route(user_data: dict, request: Request, db: Session = Depends(get_db)):
    email = user_data.get("email")
    password = user_data.get("password")
    usuario = validate_usuario(db, email=email, password=password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear una sesión segura
    session_id = secrets.token_urlsafe(32)
    access_token = secrets.token_urlsafe(32)
    token_expiry = int((datetime.now() + timedelta(minutes=30)).timestamp())

    # Almacenar datos en la sesión
    request.session.update({
        "user_id": usuario.id,
        "user_name": usuario.Nombre ,
        "user_type":usuario.Tipo_Usuarios_id,
        "session_id": session_id,
        "access_token": access_token,
        "token_expiry": token_expiry,
    })
    print("DATOS DEL REQUEST",request)
    # Almacenar el session_id en una cookie
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="Authorization", value=session_id, httponly=True, secure=True)
    return response


@router.post("/", response_model=UsuarioResponse)
def create_new_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return create_usuario(db=db, usuario=usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_existing_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db, usuario_id=usuario_id, usuario_data=usuario_data)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario


@router.delete("/{usuario_id}")
def delete_usuario_route(usuario_id: int, db: Session = Depends(get_db)):
    return delete_usuario(db, usuario_id=usuario_id)