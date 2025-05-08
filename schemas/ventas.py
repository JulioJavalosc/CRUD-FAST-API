from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class VentaCreate(BaseModel):
    Fecha: datetime
    Clientes_id: int
    total: int
    estado: int = 1  # Por defecto, las ventas son "Pendientes" (1)
    Usuarios_id: int


class VentaResponse(BaseModel):
    idVenta: int
    Fecha: datetime
    Clientes_id: int
    total: int
    estado: int  # 0 = Cancelado, 1 = Pendiente, 2 = Completado
    Usuarios_id: int

    class Config:
        from_attributes = True


class VentaUpdate(BaseModel):
    Fecha: Optional[datetime] = None
    Clientes_id: Optional[int] = None
    total: Optional[int] = None
    estado: Optional[int] = None  # Actualizar estado (opcional)
    Usuarios_id: Optional[int] = None