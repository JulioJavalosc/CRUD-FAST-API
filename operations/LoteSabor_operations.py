from sqlalchemy.orm import Session
from models import LotesSaboresBase
from schemas.LoteSabor import LoteSaborCreate


def create_lote(db: Session, lote: LoteSaborCreate):
    db_lote = LotesSaboresBase(
        id_sabor=lote.id_sabor,
        peso_total_gr=lote.peso_total_gr,
        peso_disponible_gr=lote.peso_total_gr,  
        numero_lote=lote.numero_lote
    )
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote


def get_lote(db: Session, id_lote: int):
    return db.query(LotesSaboresBase).filter(LotesSaboresBase.id_lote == id_lote).first()


def get_all_lotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LotesSaboresBase).offset(skip).limit(limit).all()


def update_lote(db: Session, id_lote: int, lote: LoteSaborCreate):
    db_lote = get_lote(db, id_lote=id_lote)
    if not db_lote:
        return None

    db_lote.id_sabor = lote.id_sabor
    db_lote.peso_total_gr = lote.peso_total_gr
    db_lote.peso_disponible_gr = lote.peso_total_gr  
    db_lote.numero_lote = lote.numero_lote

    db.commit()
    db.refresh(db_lote)
    return db_lote


def delete_lote(db: Session, id_lote: int):
    db_lote = get_lote(db, id_lote=id_lote)
    if not db_lote:
        return None
    db.delete(db_lote)
    db.commit()
    return db_lote