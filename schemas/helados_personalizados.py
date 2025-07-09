from pydantic import BaseModel
from typing import Optional, List


class HeladoPersonalizadoCreate(BaseModel):
    precio_total: int


class HeladoPersonalizadoResponse(BaseModel):
    idHelado: int
    precio_total: int

    class Config:
        from_attributes = True


class HeladoPersonalizadoUpdate(BaseModel):
    precio_total: Optional[int] = None


from pydantic import BaseModel
from typing import List

class SaborHelado(BaseModel):
    id_Sabor: int
    Cantidad_Bolas: int

class HeladoPersonalizado(BaseModel):
    sabores: List[SaborHelado]
    cantidad: int
    precio: float