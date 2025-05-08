from fastapi import HTTPException
from models import DetalleHeladoPersonalizado
from schemas.detalle_helado_personalizado import DetalleHeladoPersonalizadoCreate, DetalleHeladoPersonalizadoUpdate
from sqlalchemy.orm import Session


def get_detalles_helado_personalizado(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetalleHeladoPersonalizado).offset(skip).limit(limit).all()


def get_detalle_helado_personalizado(db: Session, detalle_id: int):
    return db.query(DetalleHeladoPersonalizado).filter(DetalleHeladoPersonalizado.idDetalle_Helado_Personalizado == detalle_id).first()


def create_detalle_helado_personalizado(db: Session, detalle: DetalleHeladoPersonalizadoCreate):
    db_detalle = DetalleHeladoPersonalizado(
        idHelado=detalle.idHelado,
        id_Sabor=detalle.id_Sabor,
        Cantidad_Bolas=detalle.Cantidad_Bolas
    )
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def update_detalle_helado_personalizado(db: Session, detalle_id: int, detalle_data: DetalleHeladoPersonalizadoUpdate):
    db_detalle = db.query(DetalleHeladoPersonalizado).filter(DetalleHeladoPersonalizado.idDetalle_Helado_Personalizado == detalle_id).first()
    if db_detalle:
        db_detalle.idHelado = detalle_data.idHelado if detalle_data.idHelado is not None else db_detalle.idHelado
        db_detalle.id_Sabor = detalle_data.id_Sabor if detalle_data.id_Sabor is not None else db_detalle.id_Sabor
        db_detalle.Cantidad_Bolas = detalle_data.Cantidad_Bolas if detalle_data.Cantidad_Bolas is not None else db_detalle.Cantidad_Bolas
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_helado_personalizado(db: Session, detalle_id: int):
    db_detalle = db.query(DetalleHeladoPersonalizado).filter(DetalleHeladoPersonalizado.idDetalle_Helado_Personalizado == detalle_id).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de helado personalizado not found")
    db.delete(db_detalle)
    db.commit()
    return {"message": "Detalle de helado personalizado deleted successfully"}