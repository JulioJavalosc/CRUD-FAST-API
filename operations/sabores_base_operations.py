from models import SaboresBase
from sqlalchemy.orm import Session


def get_sabores_base(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SaboresBase).offset(skip).limit(limit).all()


def get_sabor_base(db: Session, sabor_id: int):
    return db.query(SaboresBase).filter(SaboresBase.id_Sabor == sabor_id).first()


def create_sabor_base(db: Session, Nombre: str, Precio: int):
    db_sabor = SaboresBase(Nombre=Nombre, Precio=Precio)
    db.add(db_sabor)
    db.commit()
    db.refresh(db_sabor)
    return db_sabor


def update_sabor_base(db: Session, sabor_id: int, Nombre: str = None, Precio: int = None):
    db_sabor = get_sabor_base(db, sabor_id)
    if not db_sabor:
        return None
    if Nombre:
        db_sabor.Nombre = Nombre
    if Precio:
        db_sabor.Precio = Precio
    db.commit()
    db.refresh(db_sabor)
    return db_sabor


def delete_sabor_base(db: Session, sabor_id: int):
    db_sabor = get_sabor_base(db, sabor_id)
    if not db_sabor:
        return None
    db.delete(db_sabor)
    db.commit()
    return {"message": "Sabor eliminado"}