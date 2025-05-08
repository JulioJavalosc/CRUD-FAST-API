from fastapi import HTTPException
from models import Ventas
from schemas.ventas import VentaCreate, VentaUpdate
from sqlalchemy.orm import Session


def get_ventas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ventas).offset(skip).limit(limit).all()


def get_venta(db: Session, venta_id: int):
    return db.query(Ventas).filter(Ventas.idVenta == venta_id).first()


def create_venta(db: Session, venta: VentaCreate):
    db_venta = Ventas(
        Fecha=venta.Fecha,
        Clientes_id=venta.Clientes_id,
        total=venta.total,
        estado=venta.estado,
        Usuarios_id=venta.Usuarios_id
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta


def update_venta(db: Session, venta_id: int, venta_data: VentaUpdate):
    db_venta = db.query(Ventas).filter(Ventas.idVenta == venta_id).first()
    if db_venta:
        db_venta.Fecha = venta_data.Fecha if venta_data.Fecha is not None else db_venta.Fecha
        db_venta.Clientes_id = venta_data.Clientes_id if venta_data.Clientes_id is not None else db_venta.Clientes_id
        db_venta.total = venta_data.total if venta_data.total is not None else db_venta.total
        db_venta.estado = venta_data.estado if venta_data.estado is not None else db_venta.estado
        db_venta.Usuarios_id = venta_data.Usuarios_id if venta_data.Usuarios_id is not None else db_venta.Usuarios_id
        db.commit()
        db.refresh(db_venta)
    return db_venta


def delete_venta(db: Session, venta_id: int):
    raise HTTPException(status_code=405, detail="Las ventas no pueden eliminarse. Use la opción de anulación.")


def anular_venta(db: Session, venta_id: int):
    db_venta = db.query(Ventas).filter(Ventas.idVenta == venta_id).first()
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta not found")
    if db_venta.estado == 0:
        raise HTTPException(status_code=400, detail="La venta ya está anulada")
    db_venta.estado = 0  # Marcar como anulada
    db.commit()
    db.refresh(db_venta)
    return {"message": "Venta anulada exitosamente"}