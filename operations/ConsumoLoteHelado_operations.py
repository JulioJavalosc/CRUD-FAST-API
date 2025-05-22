from sqlalchemy.orm import Session
from models import ConsumoLoteHelado
from schemas.ConsumoLoteHelado import ConsumoLoteHeladoCreate

def crear_consumo(db: Session, consumo: ConsumoLoteHeladoCreate):
    db_consumo = ConsumoLoteHelado(**consumo.model_dump())
    db.add(db_consumo)
    db.commit()
    db.refresh(db_consumo)
    return db_consumo

def obtener_consumo(db: Session, id_consumo: int):
    return db.query(ConsumoLoteHelado).filter(ConsumoLoteHelado.id_consumo == id_consumo).first()

def obtener_consumos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConsumoLoteHelado).offset(skip).limit(limit).all()

def eliminar_consumo(db: Session, id_consumo: int):
    db_consumo = obtener_consumo(db, id_consumo=id_consumo)
    if not db_consumo:
        return None
    db.delete(db_consumo)
    db.commit()
    return db_consumo