from pydantic import BaseModel
from typing import Optional, List


class DetalleHeladoPersonalizadoCreate(BaseModel):
    idHelado: int
    id_Sabor: int
    Cantidad_Bolas: int


class DetalleHeladoPersonalizadoResponse(BaseModel):
    idDetalle_Helado_Personalizado: int
    idHelado: int
    id_Sabor: int
    Cantidad_Bolas: int

    class Config:
        from_attributes = True


class DetalleHeladoPersonalizadoUpdate(BaseModel):
    idHelado: Optional[int] = None
    id_Sabor: Optional[int] = None
    Cantidad_Bolas: Optional[int] = None