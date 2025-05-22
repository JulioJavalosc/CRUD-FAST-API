from datetime import datetime
from fastapi import HTTPException
from models import ProductosFijos,MovimientosStock
from schemas.productos_fijos import ProductoFijoCreate, ProductoFijoUpdate
from sqlalchemy.orm import Session


def get_productos_fijos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProductosFijos).offset(skip).limit(limit).all()


def get_producto_fijo(db: Session, producto_id: int):
    return db.query(ProductosFijos).filter(ProductosFijos.idProducto == producto_id).first()


def create_producto_fijo(db: Session, producto: ProductoFijoCreate):
    # Crear el producto
    db_producto = ProductosFijos(
        Descripcion=producto.Descripcion,
        Precio=producto.Precio,
        Stock=producto.Stock
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    movimiento = MovimientosStock(
        Cantidad=producto.Stock,  
        Fecha=datetime.now(),    
        Tipo_Movimiento=1,       
        idProducto=db_producto.idProducto,  
        idUsuario=producto.idUsuario          #
    )
    db.add(movimiento)
    db.commit()

    return db_producto


def update_producto_fijo(db: Session, producto_id: int, producto_data: ProductoFijoUpdate, usuario_id: int = None):
    db_producto = db.query(ProductosFijos).filter(ProductosFijos.idProducto == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto_data.Descripcion:
        db_producto.Descripcion = producto_data.Descripcion
    if producto_data.Precio is not None:
        db_producto.Precio = producto_data.Precio
    if producto_data.Stock is not None:
        diferencia = producto_data.Stock - db_producto.Stock
        db_producto.Stock = producto_data.Stock

        # Registrar movimiento
        tipo_movimiento = 1 if diferencia > 0 else 2
        movimiento = MovimientosStock(
            Cantidad=abs(diferencia),
            Fecha=datetime.now(),
            Tipo_Movimiento=tipo_movimiento,
            idProducto=db_producto.idProducto,
            idUsuario=usuario_id or 1  # Reemplaza por sesión si es posible
        )
        db.add(movimiento)

    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_producto_fijo(db: Session, producto_id: int):
    db_producto = db.query(ProductosFijos).filter(ProductosFijos.idProducto == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto fijo not found")
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto fijo deleted successfully"}

def actualizar_stock_producto(db: Session, producto_id: int, nueva_cantidad: int , usuario_id:int):
    # Obtener el producto
    producto = db.query(ProductosFijos).filter(ProductosFijos.idProducto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Determinar si es una entrada o salida
    tipo_movimiento = 1 if nueva_cantidad > producto.Stock else 2
    # Calcular la diferencia de stock
    diferencia = abs(nueva_cantidad - producto.Stock)

    # Actualizar el stock del producto
    producto.Stock = nueva_cantidad
    db.commit()

    # Registrar el movimiento en la tabla Movimientos_Stock
    movimiento = MovimientosStock(
        Cantidad=str(diferencia),
        Fecha=datetime.now(),
        Tipo_Movimiento=tipo_movimiento,  # 1 = Entrada, 2 = Salida
        idProducto=producto_id,
        idUsuario=usuario_id
    )
    db.add(movimiento)
    db.commit()

    return {"message": "Stock actualizado y movimiento registrado correctamente"}