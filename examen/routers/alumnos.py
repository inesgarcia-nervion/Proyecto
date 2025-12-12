from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .auth_users import authentication


router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

class Alumnos(BaseModel):
    id: int
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    curso: str
    repetidor : bool
    id_colegio : int
    
alumnos_list = [
    Alumnos(id=1, nombre="Inés ", apellidos="Garcia Chamorro", fecha_nacimiento="01-10-2001",curso="2DAM", repetidor=False, id_colegio=1),
    Alumnos(id=2, nombre="Dylan ", apellidos="Cano Torres", fecha_nacimiento="25-11-1999",curso="1DAM", repetidor=False, id_colegio=2),
    Alumnos(id=3, nombre="Ángela ", apellidos="Garcia Chamorro", fecha_nacimiento="01-12-1997",curso="1BACH", repetidor=True, id_colegio=3),
    Alumnos(id=4, nombre="Paula ", apellidos="Dominguez Tejada", fecha_nacimiento="05-05-2000",curso="2BACH", repetidor=False, id_colegio=1),
    Alumnos(id=5, nombre="Alejandro ", apellidos="Gallardo Cuevas", fecha_nacimiento="06-04-2001",curso="2DAM", repetidor=True, id_colegio=2),
]


#GET
@router.get("", status_code=200)
def alumnos():
    alumnos = alumnos_list
    if alumnos:
        return alumnos


#FALTA EL CURSO Y DISTRITO
#GET
@router.get("{id_alumno}")
def get_alumno_query(id : int):
    return search_alumno(id)

def search_alumno(id : int):
    alumnos = [alumno for alumno in alumnos_list if alumno.id == id]
    
    if not alumnos:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumnos[0]






#FALTA EL ID DE COLEGIO Y CURSO VALIDO
#POST
@router.post("/", status_code=201, response_model= Alumnos)
def add_alumno(alumno : Alumnos, authorized = Depends(authentication)):
    alumno.id = next_id()
    alumnos_list.append(alumno)
    return alumno

def next_id():
    return(max(alumnos_list, key=id).id+1)



#FALTA ID DE COLEGIO
#PUT
@router.put("/{id_alumno}")
def modify_alumno(id:int, alumno:Alumnos, authorized = Depends(authentication)):
    for index, saved_alumno in enumerate(alumnos_list):
        if saved_alumno.id == id:
            alumno.id = id
            alumnos_list[index] = alumno
            return alumno
        raise HTTPException(status_code=200, detail="Se ha actualizado correctamente")
    raise HTTPException(status_code=404, detail="Alumno no encontrado")


#DELETE 
@router.delete("/{id_alumno}")
def remove_alumno(id : int):
    for saved_alumno in alumnos_list:
        if saved_alumno.id == id:
            alumnos_list.remove(saved_alumno)
            return{}
        raise HTTPException(status_code=200, detail="Se ha eliminado correctamente")
    raise HTTPException(status_code=404, detail="Alumno no encontrado")