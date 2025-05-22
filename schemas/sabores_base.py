from pydantic import BaseModel
from typing import Optional, List


class SaborBaseCreate(BaseModel):
    Nombre: str
    Precio: int


class SaborBaseResponse(BaseModel):
    id_Sabor: int
    Nombre: str
    Precio: int
    class Config:
        from_attributes = True


class SaborBaseUpdate(BaseModel):
    Nombre: Optional[str] = None
    Precio: Optional[int] = None