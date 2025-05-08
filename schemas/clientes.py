from pydantic import BaseModel
from typing import Optional, List


class ClienteCreate(BaseModel):
    Nombre: str
    Apellido: Optional[str] = None
    telefono: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    Nombre: str
    Apellido: Optional[str] = None
    telefono: Optional[str] = None

    class Config:
        from_attributes = True


class ClienteUpdate(BaseModel):
    Nombre: Optional[str] = None
    Apellido: Optional[str] = None
    telefono: Optional[str] = None