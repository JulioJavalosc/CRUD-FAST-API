from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UsuarioCreate(BaseModel):
    Nombre: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    Tipo_Usuarios_id: int


class UsuarioResponse(BaseModel):
    id: int
    Nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    Tipo_Usuarios_id: int

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    Nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    Tipo_Usuarios_id: Optional[int] = None


class UsuarioValidate(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True