from fastapi import HTTPException
from models import SaboresBase
from schemas.sabores_base import SaborBaseCreate, SaborBaseUpdate
from sqlalchemy.orm import Session


def get_sabores_base(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SaboresBase).offset(skip).limit(limit).all()


def get_sabor_base(db: Session, sabor_id: int):
    return db.query(SaboresBase).filter(SaboresBase.id_Sabor == sabor_id).first()


def create_sabor_base(db: Session, sabor: SaborBaseCreate):
    db_sabor = SaboresBase(
        Nombre=sabor.Nombre,
        Precio=sabor.Precio,
        Stock=sabor.Stock
    )
    db.add(db_sabor)
    db.commit()
    db.refresh(db_sabor)
    return db_sabor


def update_sabor_base(db: Session, sabor_id: int, sabor_data: SaborBaseUpdate):
    db_sabor = db.query(SaboresBase).filter(SaboresBase.id_Sabor == sabor_id).first()
    if db_sabor:
        db_sabor.Nombre = sabor_data.Nombre if sabor_data.Nombre is not None else db_sabor.Nombre
        db_sabor.Precio = sabor_data.Precio if sabor_data.Precio is not None else db_sabor.Precio
        db_sabor.Stock = sabor_data.Stock if sabor_data.Stock is not None else db_sabor.Stock
        db.commit()
        db.refresh(db_sabor)
    return db_sabor


def delete_sabor_base(db: Session, sabor_id: int):
    db_sabor = db.query(SaboresBase).filter(SaboresBase.id_Sabor == sabor_id).first()
    if not db_sabor:
        raise HTTPException(status_code=404, detail="Sabor base not found")
    db.delete(db_sabor)
    db.commit()
    return {"message": "Sabor base deleted successfully"}