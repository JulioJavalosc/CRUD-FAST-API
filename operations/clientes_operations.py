from fastapi import HTTPException
from models import Clientes
from schemas.clientes import ClienteCreate, ClienteUpdate
from sqlalchemy.orm import Session


def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Clientes).offset(skip).limit(limit).all()


def get_cliente(db: Session, cliente_id: int):
    return db.query(Clientes).filter(Clientes.id == cliente_id).first()


def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Clientes(
        Nombre=cliente.Nombre,
        Apellido=cliente.Apellido,
        telefono=cliente.telefono
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def update_cliente(db: Session, cliente_id: int, cliente_data: ClienteUpdate):
    db_cliente = db.query(Clientes).filter(Clientes.id == cliente_id).first()
    if db_cliente:
        db_cliente.Nombre = cliente_data.Nombre if cliente_data.Nombre is not None else db_cliente.Nombre
        db_cliente.Apellido = cliente_data.Apellido if cliente_data.Apellido is not None else db_cliente.Apellido
        db_cliente.telefono = cliente_data.telefono if cliente_data.telefono is not None else db_cliente.telefono
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(Clientes).filter(Clientes.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente deleted successfully"}