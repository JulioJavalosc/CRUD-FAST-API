from fastapi import HTTPException
from models import TipoUsuarios
from schemas.tipo_usuarios import TipoUsuarioCreate, TipoUsuarioUpdate
from sqlalchemy.orm import Session


def get_tipo_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TipoUsuarios).filter(TipoUsuarios.activo == True).offset(skip).limit(limit).all()


def get_tipo_usuario(db: Session, tipo_usuario_id: int):
    return db.query(TipoUsuarios).filter(TipoUsuarios.id == tipo_usuario_id).first()


def create_tipo_usuario(db: Session, tipo_usuario: TipoUsuarioCreate):
    db_tipo_usuario = TipoUsuarios(
        Nombre=tipo_usuario.Nombre,
        activo=tipo_usuario.activo
    )
    db.add(db_tipo_usuario)
    db.commit()
    db.refresh(db_tipo_usuario)
    return db_tipo_usuario


def update_tipo_usuario(db: Session, tipo_usuario_id: int, tipo_usuario_data: TipoUsuarioUpdate):
    db_tipo_usuario = db.query(TipoUsuarios).filter(TipoUsuarios.id == tipo_usuario_id).first()
    if db_tipo_usuario:
        db_tipo_usuario.Nombre = tipo_usuario_data.Nombre if tipo_usuario_data.Nombre is not None else db_tipo_usuario.Nombre
        db_tipo_usuario.activo = tipo_usuario_data.activo if tipo_usuario_data.activo is not None else db_tipo_usuario.activo
        db.commit()
        db.refresh(db_tipo_usuario)
    return db_tipo_usuario


def delete_tipo_usuario(db: Session, tipo_usuario_id: int):
    db_tipo_usuario = db.query(TipoUsuarios).filter(TipoUsuarios.id == tipo_usuario_id).first()
    if not db_tipo_usuario:
        raise HTTPException(status_code=404, detail="Tipo de usuario not found")
    db.delete(db_tipo_usuario)
    db.commit()
    return {"message": "Tipo de usuario deleted successfully"}