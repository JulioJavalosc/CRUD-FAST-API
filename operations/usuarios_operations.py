import bcrypt
from fastapi import HTTPException
from models import Usuarios
from schemas.user import UsuarioCreate, UsuarioUpdate, UsuarioValidate
from sqlalchemy.orm import Session


def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuarios).offset(skip).limit(limit).all()


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuarios).filter(Usuarios.id == usuario_id).first()


def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuarios(
        Nombre=usuario.Nombre,
        telefono=usuario.telefono,
        email=usuario.email,
        password=usuario.password,
        Tipo_Usuarios_id=usuario.Tipo_Usuarios_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if db_usuario:
        db_usuario.Nombre = usuario_data.Nombre if usuario_data.Nombre is not None else db_usuario.Nombre
        db_usuario.telefono = usuario_data.telefono if usuario_data.telefono is not None else db_usuario.telefono
        db_usuario.email = usuario_data.email if usuario_data.email is not None else db_usuario.email
        db_usuario.password = usuario_data.password if usuario_data.password is not None else db_usuario.password
        db_usuario.Tipo_Usuarios_id = usuario_data.Tipo_Usuarios_id if usuario_data.Tipo_Usuarios_id is not None else db_usuario.Tipo_Usuarios_id
        db.commit()
        db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuario deleted successfully"}


def validate_usuario(db: Session, email: str, password: str):
    db_usuario = db.query(Usuarios).filter(
        Usuarios.email == email,
        Usuarios.activo == True
    ).first()

    if db_usuario and bcrypt.checkpw(password.encode('utf-8'), db_usuario.password.encode('utf-8')):
        print("USUARIO VÁLIDO")
        return db_usuario
    else:
        print("USUARIO INEXISTENTE O CONTRASEÑA INVÁLIDA")
        return None
