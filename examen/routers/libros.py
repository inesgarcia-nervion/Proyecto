#AUTOR Y LIBROS:
#AUTOR(Id, DNI, Nombre, Apellidos)
#LIBRO(Id, ISBN, Título, NumPaginas, IdAutor)
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .auth_users import authentication


router = APIRouter(prefix="/libros", tags=["Libros"])

class Libros(BaseModel):
    id: int
    ISBN: str
    Título: str
    NumPaginas: int
    IdAutor: int

libros_list = [
    Libros(id=1, ISBN="978-3-16-148410-0", Título="Cien Años de Soledad", NumPaginas=417, IdAutor=1),
    Libros(id=2, ISBN="978-0-14-118506-4", Título="1984", NumPaginas=328, IdAutor=2),
    Libros(id=3, ISBN="978-0-452-28423-4", Título="El Gran Gatsby", NumPaginas=180, IdAutor=3),
    Libros(id=4, ISBN="978-0-7432-7356-5", Título="To Kill a Mockingbird", NumPaginas=281, IdAutor=4),
    Libros(id=5, ISBN="978-0-679-73232-3", Título="The Catcher in the Rye", NumPaginas=214, IdAutor=5),
]   


#GET
@router.get("/")
def libros():
    return libros_list

@router.get("/{id_libro}")
def get_libro(id_libro : int):
    return search_libro(id_libro)


#GET con query
@router.get("")
def get_libro_query(id : int):
    return search_libro(id)


def search_libro(id : int):
    libros = [libro for libro in libros_list if libro.id == id]

    if not libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros[0]



#POST 
@router.post("/", status_code=201, response_model= Libros)
def add_libro(libro : Libros, authorized = Depends(authentication)):
    libro.id = next_id()
    libros_list.append(libro)
    return libro

def next_id():
    return(max(libros_list, key=id).id+1)


#PUT
@router.put("/{id}")
def modify_libro(id : int, libro: Libros):
    for index, saved_libro in enumerate(libros_list):
        if saved_libro.id == id:
            libro.id = id
            libros_list[index] = libro
            return libro

    raise HTTPException(status_code=404, detail="Libro no encontrado")


#DELETE 
@router.delete("/{id}")
def remove_libro(id : int):
    for saved_libro in libros_list:
        if saved_libro.id == id:
            libros_list.remove(saved_libro)
            return{}
    
    raise HTTPException(status_code=404, detail="Libro no encontrado")