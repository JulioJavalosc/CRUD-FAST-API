from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.ConsumoLoteHelado import ConsumoLoteHeladoCreate, ConsumoLoteHeladoResponse
from operations.ConsumoLoteHelado_operations import (
    crear_consumo,
    obtener_consumo,
    obtener_consumos,
    eliminar_consumo
)

router = APIRouter(
    prefix="/consumos-lote",
    tags=["Consumos de Lote"]
)

@router.post("/", response_model=ConsumoLoteHeladoResponse)
def registrar_consumo(consumo: ConsumoLoteHeladoCreate, db: Session = Depends(get_db)):
    return crear_consumo(db, consumo)

@router.get("/{id_consumo}", response_model=ConsumoLoteHeladoResponse)
def leer_consumo(id_consumo: int, db: Session = Depends(get_db)):
    db_consumo = obtener_consumo(db, id_consumo=id_consumo)
    if not db_consumo:
        raise HTTPException(status_code=404, detail="Consumo no encontrado")
    return db_consumo

@router.get("/", response_model=list[ConsumoLoteHeladoResponse])
def listar_consumos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return obtener_consumos(db, skip=skip, limit=limit)

@router.delete("/{id_consumo}", response_model=ConsumoLoteHeladoResponse)
def borrar_consumo(id_consumo: int, db: Session = Depends(get_db)):
    db_consumo = eliminar_consumo(db, id_consumo=id_consumo)
    if not db_consumo:
        raise HTTPException(status_code=404, detail="Consumo no encontrado")
    return db_consumo