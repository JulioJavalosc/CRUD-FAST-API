from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Clientes

router = APIRouter(tags=["Clientes"])

@router.post("/clientes/guardar-ajax")
def guardar_cliente_ajax(
    Nombre: str = Form(...),
    Apellido: str = Form(None),
    telefono: str = Form(None),
    db: Session = Depends(get_db)
):
    # Guardar cliente en BD
    nuevo_cliente = Clientes(Nombre=Nombre, Apellido=Apellido, telefono=telefono)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    # Devolver JSON para actualizar select
    return {
        "id": nuevo_cliente.id,
        "Nombre": nuevo_cliente.Nombre
    }