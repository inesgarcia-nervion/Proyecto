from typing import Optional
from pydantic import BaseModel


# Entidad Jugador
class Jugadores(BaseModel):
    id: Optional[str] = None
    Nombre: str
    Edad: int
    Posición: str
    Nacionalidad: str
    Salario: float  
    idEquipo: int