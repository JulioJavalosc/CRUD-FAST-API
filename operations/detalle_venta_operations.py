from fastapi import HTTPException
from models import DetalleVenta
from schemas.detalle_venta import DetalleVentaCreate, DetalleVentaUpdate
from sqlalchemy.orm import Session


def get_detalles_venta(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetalleVenta).offset(skip).limit(limit).all()


def get_detalle_venta(db: Session, detalle_id: int):
    return db.query(DetalleVenta).filter(DetalleVenta.idDetalle_Venta == detalle_id).first()


def create_detalle_venta(db: Session, detalle: DetalleVentaCreate):
    db_detalle = DetalleVenta(
        Cantidad=detalle.Cantidad,
        subtotal=detalle.subtotal,
        idVenta=detalle.idVenta,
        idProducto=detalle.idProducto,
        idHelado=detalle.idHelado
    )
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def update_detalle_venta(db: Session, detalle_id: int, detalle_data: DetalleVentaUpdate):
    db_detalle = db.query(DetalleVenta).filter(DetalleVenta.idDetalle_Venta == detalle_id).first()
    if db_detalle:
        db_detalle.Cantidad = detalle_data.Cantidad if detalle_data.Cantidad is not None else db_detalle.Cantidad
        db_detalle.subtotal = detalle_data.subtotal if detalle_data.subtotal is not None else db_detalle.subtotal
        db_detalle.idProducto = detalle_data.idProducto if detalle_data.idProducto is not None else db_detalle.idProducto
        db_detalle.idHelado = detalle_data.idHelado if detalle_data.idHelado is not None else db_detalle.idHelado
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_venta(db: Session, detalle_id: int):
    db_detalle = db.query(DetalleVenta).filter(DetalleVenta.idDetalle_Venta == detalle_id).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta not found")
    db.delete(db_detalle)
    db.commit()
    return {"message": "Detalle de venta deleted successfully"}