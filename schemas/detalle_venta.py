from pydantic import BaseModel
from typing import Optional, List


class DetalleVentaCreate(BaseModel):
    Cantidad: int
    subtotal: int
    idVenta: int
    idProducto: Optional[int] = None
    idHelado: Optional[int] = None


class DetalleVentaResponse(BaseModel):
    idDetalle_Venta: int
    Cantidad: int
    subtotal: int
    idVenta: int
    idProducto: Optional[int] = None
    idHelado: Optional[int] = None

    class Config:
        from_attributes = True


class DetalleVentaUpdate(BaseModel):
    Cantidad: Optional[int] = None
    subtotal: Optional[int] = None
    idProducto: Optional[int] = None
    idHelado: Optional[int] = None