from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])   

class Jugadores(BaseModel):
    id: int
    Nombre: str
    Edad: int
    Posición: str
    Nacionalidad: str
    Salario: float  
    idEquipo: int


jugadores_list = [
    Jugadores(id=1, Nombre="Lionel Messi", Edad=36, Posición="Delantero", Nacionalidad="Argentina", Salario=41000000.0, idEquipo=1),
    Jugadores(id=2, Nombre="Cristiano Ronaldo", Edad=39, Posición="Delantero", Nacionalidad="Portugal", Salario=50000000.0, idEquipo=3),
    Jugadores(id=3, Nombre="Neymar Jr.", Edad=32, Posición="Delantero", Nacionalidad="Brasil", Salario=36000000.0, idEquipo=4),
    Jugadores(id=4, Nombre="Kylian Mbappé", Edad=25, Posición="Delantero", Nacionalidad="Francia", Salario=22000000.0, idEquipo=2),
    Jugadores(id=5, Nombre="Kevin De Bruyne", Edad=32, Posición="Centrocampista", Nacionalidad="Bélgica", Salario=20000000.0, idEquipo=3),
    Jugadores(id=6, Nombre="Robert Lewandowski", Edad=35, Posición="Delantero", Nacionalidad="Polonia", Salario=25000000.0, idEquipo=2),
]



#GET
@router.get("/")
def jugadores():
    return jugadores_list


@router.get("/{id_jugador}")
def get_jugador(id_jugador : int):
    return search_jugador(id_jugador)


@router.get("/query/")                  
def get_jugador(id : int):
    return search_jugador(id)



def search_jugador(idEquipo : int):
    return [jugador for jugador in jugadores_list if jugador.idEquipo == idEquipo]
    
    
    #jugadores = [jugador for jugador in jugadores_list if jugador.id == id]

    #if not jugadores:
    #    raise HTTPException(status_code=404, detail="Jugador no encontrado")
    #return jugadores[0]






#POST 
@router.post("/", status_code=201, response_model= Jugadores)
def add_jugador(jugador : Jugadores):
    jugador.id = next_id()
    jugadores_list.append(jugador)
    return jugador

def next_id():
    return(max(jugadores_list, key=id).id+1)


#PUT
@router.put("/{id}")
def modify_jugador(id:int, jugador:Jugadores):
    for index, saved_jugador in enumerate(jugadores_list):
        if saved_jugador.id == id:
            jugador.id = id
            jugadores_list[index] = jugador
            return jugador

    raise HTTPException(status_code=404, detail="Jugador no encontrado")



#DELETE
@router.delete("/{id}")
def remove_jugador(id : int):
    for saved_jugador in jugadores_list:
        if saved_jugador.id == id:
            jugadores_list.remove(saved_jugador)
            return{}
        
    raise HTTPException(status_code=404, detail="Jugador no encontrado")