from pydantic import BaseModel
from typing import Optional

class ConsumoLoteHeladoBase(BaseModel):
    id_detalle_helado: int
    id_lote: int
    cantidad_utilizada_gr: int

class ConsumoLoteHeladoCreate(ConsumoLoteHeladoBase):
    pass

class ConsumoLoteHeladoResponse(ConsumoLoteHeladoBase):
    id_consumo: int

    class Config:
        from_attributes = True