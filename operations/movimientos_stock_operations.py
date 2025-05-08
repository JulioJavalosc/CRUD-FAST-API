from fastapi import HTTPException
from models import MovimientosStock,ProductosFijos, Usuarios
from schemas.movimientos_stock import MovimientoStockCreate, MovimientoStockUpdate
from sqlalchemy.orm import Session


from datetime import datetime

def get_movimientos_stock(db: Session, skip: int = 0, limit: int = 10):
    # Realizar un JOIN entre MovimientosStock y ProductosFijos
    query = (
        db.query(
            MovimientosStock,
            ProductosFijos.Descripcion.label("NombreProducto"),
            Usuarios.Nombre.label("NombreUsuario") 
        )
        .outerjoin(ProductosFijos, MovimientosStock.idProducto == ProductosFijos.idProducto)
        .outerjoin(Usuarios, MovimientosStock.idUsuario == Usuarios.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Transformar los resultados para incluir el nombre del producto y formatear la fecha
    movimientos_con_nombre = []
    for movimiento, descripcion_producto , nombre_usuario in query:
        movimiento_dict = movimiento.__dict__
        movimiento_dict["NombreProducto"] = descripcion_producto  # Asignar el valor de "Descripcion"
        movimiento_dict["NombreUsuario"] = nombre_usuario
        # Formatear la fecha en un formato legible
        if movimiento_dict["Fecha"]:
            movimiento_dict["Fecha"] = movimiento_dict["Fecha"].strftime("%d/%m/%Y %H:%M:%S")

        movimientos_con_nombre.append(movimiento_dict)

    return movimientos_con_nombre


def get_movimiento_stock(db: Session, movimiento_id: int):
    return db.query(MovimientosStock).filter(MovimientosStock.id == movimiento_id).first()


def create_movimiento_stock(db: Session, movimiento: MovimientoStockCreate):
    if movimiento.Tipo_Movimiento not in [1, 2]:
        raise HTTPException(status_code=400, detail="Tipo_Movimiento debe ser 1 (Entrada) o 2 (Salida)")

    db_movimiento = MovimientosStock(
        Cantidad=movimiento.Cantidad,
        Fecha=movimiento.Fecha,
        Tipo_Movimiento=movimiento.Tipo_Movimiento,
        id_Sabor=movimiento.id_Sabor,
        idProducto=movimiento.idProducto,
        idUsuario=movimiento.idUsuario
    )
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def update_movimiento_stock(db: Session, movimiento_id: int, movimiento_data: MovimientoStockUpdate):
    db_movimiento = db.query(MovimientosStock).filter(MovimientosStock.id == movimiento_id).first()
    if db_movimiento:
        db_movimiento.Cantidad = movimiento_data.Cantidad if movimiento_data.Cantidad is not None else db_movimiento.Cantidad
        db_movimiento.Fecha = movimiento_data.Fecha if movimiento_data.Fecha is not None else db_movimiento.Fecha
        db_movimiento.Tipo_Movimiento = movimiento_data.Tipo_Movimiento if movimiento_data.Tipo_Movimiento is not None else db_movimiento.Tipo_Movimiento
        db_movimiento.id_Sabor = movimiento_data.id_Sabor if movimiento_data.id_Sabor is not None else db_movimiento.id_Sabor
        db_movimiento.idProducto = movimiento_data.idProducto if movimiento_data.idProducto is not None else db_movimiento.idProducto
        db.commit()
        db.refresh(db_movimiento)
    return db_movimiento


def delete_movimiento_stock(db: Session, movimiento_id: int):
    db_movimiento = db.query(MovimientosStock).filter(MovimientosStock.id == movimiento_id).first()
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento de stock not found")
    db.delete(db_movimiento)
    db.commit()
    return {"message": "Movimiento de stock deleted successfully"}