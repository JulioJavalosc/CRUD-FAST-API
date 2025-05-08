from pydantic import BaseModel
from typing import Optional, List


class TipoUsuarioCreate(BaseModel):
    Nombre: Optional[str] = None
    activo: Optional[bool] = True


class TipoUsuarioResponse(BaseModel):
    id: int
    Nombre: Optional[str] = None
    activo: bool

    class Config:
        from_attributes = True


class TipoUsuarioUpdate(BaseModel):
    Nombre: Optional[str] = None
    activo: Optional[bool] = None