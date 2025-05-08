from pydantic import BaseModel
from typing import Optional, List


class ProductoFijoCreate(BaseModel):
    Descripcion: str
    Precio: int
    Stock: int
    idUsuario: Optional[int] = None

class ProductoFijoResponse(BaseModel):
    idProducto: int
    Descripcion: str
    Precio: int
    Stock: int

    class Config:
        from_attributes = True


class ProductoFijoUpdate(BaseModel):
    Descripcion: Optional[str] = None
    Precio: Optional[int] = None
    Stock: Optional[int] = None