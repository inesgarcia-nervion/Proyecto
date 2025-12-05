from typing import Optional
from pydantic import BaseModel


# Entidad Equipo
class Equipo(BaseModel):
    id: Optional[str] = None
    Nombre: str
    Ciudad: str
    AñoFundación : int
    Estadio: str