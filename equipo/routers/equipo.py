from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .jugadores import search_jugador 


router = APIRouter(prefix="/equipo", tags=["Equipos"])     

class Equipo(BaseModel):
    id: int
    Nombre: str
    Ciudad: str
    AñoFundación : int
    Estadio: str

equipos_list = [
    Equipo(id=1, Nombre="FC Barcelona", Ciudad="Barcelona", AñoFundación=1899, Estadio="Camp Nou"),
    Equipo(id=2, Nombre="Real Madrid", Ciudad="Madrid", AñoFundación=1902, Estadio="Santiago Bernabéu"),
    Equipo(id=3, Nombre="Atlético de Madrid", Ciudad="Madrid", AñoFundación=1903, Estadio="Wanda Metropolitano"),
    Equipo(id=4, Nombre="Sevilla FC", Ciudad="Sevilla", AñoFundación=1890, Estadio="Ramón Sánchez Pizjuán"),
    Equipo(id=5, Nombre="Valencia CF", Ciudad="Valencia", AñoFundación=1919, Estadio="Mestalla"),
    Equipo(id=6, Nombre="Villarreal CF", Ciudad="Villarreal", AñoFundación=1923, Estadio="Estadio de la Cerámica"),
]

#GET
@router.get("/")
def equipos():
    return equipos_list


@router.get("/{id_equipo}")
def get_equipo(id_equipo : int):
    return search_equipo(id_equipo)


@router.get("/query/")                  
def get_equipo(id : int):
    return search_equipo(id)


def search_equipo(id : int):
    equipos = [equipo for equipo in equipos_list if equipo.id == id]

    if not equipos:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipos[0]



# PARA PODER JUNTAR LA ID DE EQUIPO CON SUS JUGADORES
# EJEMPLO DE LO QUE TENEMOS QUE PONER PARA QUE FUNCIONE http://127.0.0.1:8000/equipo/3/jugadores
@router.get("/{id}/jugadores")
def get_jugadores(id : int):
    equipo = search_equipo(id)
    #Si existe el equipo
    if equipo: 
        #Buscamos los jugadores que pertenezcan a ese equipo
        jugadores = search_jugador(id)
        if jugadores:
            return jugadores
        raise HTTPException(status_code=404, detail="El equipo {id} no tiene jugadores asignados")
    raise HTTPException(status_code=404, detail="Equipo no encontrado {id}")




#POST
@router.post("/", status_code=201, response_model= Equipo)
def add_equipo(equipo : Equipo):
    equipo.id = next_id()
    equipos_list.append(equipo)
    return equipo


def next_id():
    return(max(equipos_list, key=id).id+1)



#PUT
@router.put("/{id}")
def modify_equipo(id:int, equipo:Equipo):
    for index, saved_equipo in enumerate(equipos_list):
        if saved_equipo.id == id:
            equipo.id = id
            equipos_list[index] = equipo
            return equipo
    
    raise HTTPException(status_code=404, detail="Equipo no encontrado")



#DELETE
@router.delete("/{id}")
def remove_equipo(id : int):
    for saved_equipo in equipos_list:
        if saved_equipo.id == id:
            equipos_list.remove(saved_equipo)
            return{}
    
    raise HTTPException(status_code=404, detail="Equipo no encontrado")