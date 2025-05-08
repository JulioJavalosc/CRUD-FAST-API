from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class MovimientoStockCreate(BaseModel):
    Cantidad: int # VARCHAR(45)
    Fecha: datetime
    Tipo_Movimiento: int  # 1 = Entrada, 2 = Salida
    id_Sabor: Optional[int] = None
    idProducto: Optional[int] = None
    idUsuario: Optional[int] = None
    class Config:
        from_attributes = True


class MovimientoStockResponse(BaseModel):
    id: int
    Cantidad: int
    Fecha: datetime
    Tipo_Movimiento: int
    id_Sabor: Optional[int] = None
    idProducto: Optional[int] = None
    NombreProducto: Optional[str] = None  # Nuevo campo para el nombre del producto
    idUsuario: Optional[int] = None
    NombreUsuario: Optional[str] = None  # Nuevo campo para el nombre del usuario

    class Config:
        from_attributes = True

class MovimientoStockUpdate(BaseModel):
    Cantidad: Optional[int] = None
    Fecha: Optional[datetime] = None
    Tipo_Movimiento: Optional[int] = None
    id_Sabor: Optional[int] = None
    idProducto: Optional[int] = None

class ActualizarStockRequest(BaseModel):
    nueva_cantidad: int
    usuario_id: int