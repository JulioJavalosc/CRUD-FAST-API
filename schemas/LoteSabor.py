from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Esquema base compartido
class LoteSaborBase(BaseModel):
    id_sabor: int
    peso_total_gr: int
    numero_lote: Optional[str] = None

# Para crear un nuevo lote
class LoteSaborCreate(LoteSaborBase):
    pass

# Para respuesta del servidor
class LoteSabor(LoteSaborBase):
    id_lote: int
    fecha_ingreso: datetime  # Puedes usar datetime si lo conviertes
    peso_disponible_gr: int
    class Config:
        from_attributes = True