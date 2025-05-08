from fastapi import HTTPException
from models import HeladosPersonalizados
from schemas.helados_personalizados import HeladoPersonalizadoCreate, HeladoPersonalizadoUpdate
from sqlalchemy.orm import Session


def get_helados_personalizados(db: Session, skip: int = 0, limit: int = 10):
    return db.query(HeladosPersonalizados).offset(skip).limit(limit).all()


def get_helado_personalizado(db: Session, helado_id: int):
    return db.query(HeladosPersonalizados).filter(HeladosPersonalizados.idHelado == helado_id).first()


def create_helado_personalizado(db: Session, helado: HeladoPersonalizadoCreate):
    db_helado = HeladosPersonalizados(
        precio_total=helado.precio_total
    )
    db.add(db_helado)
    db.commit()
    db.refresh(db_helado)
    return db_helado


def update_helado_personalizado(db: Session, helado_id: int, helado_data: HeladoPersonalizadoUpdate):
    db_helado = db.query(HeladosPersonalizados).filter(HeladosPersonalizados.idHelado == helado_id).first()
    if db_helado:
        db_helado.precio_total = helado_data.precio_total if helado_data.precio_total is not None else db_helado.precio_total
        db.commit()
        db.refresh(db_helado)
    return db_helado


def delete_helado_personalizado(db: Session, helado_id: int):
    db_helado = db.query(HeladosPersonalizados).filter(HeladosPersonalizados.idHelado == helado_id).first()
    if not db_helado:
        raise HTTPException(status_code=404, detail="Helado personalizado not found")
    db.delete(db_helado)
    db.commit()
    return {"message": "Helado personalizado deleted successfully"}