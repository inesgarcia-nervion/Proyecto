from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .alumnos import search_alumno
from .auth_users import authentication

router = APIRouter(prefix="/colegios", tags=["Colegios"])

class Colegio(BaseModel):
    id: int
    nombre: str
    distrito: str
    tipo: str
    direccion: str
    
colegios_list = [
    Colegio(id=1, nombre="IES Nervion", distrito="Nervion", tipo="Publico", direccion="Calle ejemplo"),
    Colegio(id=2, nombre="IES Vedruna", distrito="Nervion", tipo="Concertado", direccion="Calle ejemplo2"),
    Colegio(id=3, nombre="IES San Jose de la Rinconada", distrito="Sevilla", tipo="Publico", direccion="Calle ejemplo3"),
    Colegio(id=4, nombre="IES Carmona", distrito="Sevilla", tipo="Publico", direccion="Calle ejemplo4")
]

#GET
@router.get("", status_code=200)
def colegios():
    colegios = colegios_list
    if colegios:
        return colegios


@router.get("/{id_colegio}")
def get_colegio(id_colegio : int):
    return search_colegio(id_colegio)

def search_colegio(id : int):
    colegios = [colegio for colegio in colegios_list if colegio.id == id]
    
    if not colegios:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return colegios[0]



#GET CON QUERY
@router.get("/{id_colegio}/alumnos")
def get_alumnos(id : int):
    colegio = search_colegio(id)
    if colegio:
        alumnos = search_alumno(id)
        if alumnos:
            return alumnos
        raise HTTPException(status_code=404, detail="El colegio no tiene alumnos asignados")
    raise HTTPException(status_code=404, detail="Colegio no encontrado")




#POST 
@router.post("/colegios", status_code=201, response_model=Colegio)
def add_colegio(colegio : Colegio, authorized = Depends(authentication)):
    colegio.id = next_id()
    colegios_list.append(colegio)
    return colegio

def next_id():
    return(max(colegios_list, key=id).id+1)


