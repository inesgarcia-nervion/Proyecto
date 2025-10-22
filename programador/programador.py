from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Programador(BaseModel):
    id: int
    DNI: str
    Nombre: str
    Apellidos: str
    Telefono: int
    Email: str

programadores_list = [
    Programador(id=1, DNI="23456789L", Nombre="Ines", Apellidos="Garcia Ruiz", Telefono=612345678, Email="ines.garcia@example.com"),
    Programador(id=2, DNI="48765903M", Nombre="Angela", Apellidos="Perez Torres", Telefono=698765432, Email="angela.perez@example.com"),
    Programador(id=3, DNI="15904827R", Nombre="Dylan", Apellidos="Cano Morales", Telefono=622334455, Email="dylan.cano@example.com"),
    Programador(id=4, DNI="76029184T", Nombre="Lucas", Apellidos="Sanchez Lopez", Telefono=644556677, Email="lucas.sanchez@example.com"),
    Programador(id=5, DNI="34567890J", Nombre="Laura", Apellidos="Martinez Diaz", Telefono=655667788, Email="laura.martinez@example.com"),
    Programador(id=6, DNI="23456712H", Nombre="Mario", Apellidos="Vega Alonso", Telefono=699887766, Email="mario.vega@example.com"),
    Programador(id=7, DNI="98765432K", Nombre="Clara", Apellidos="Santos Ruiz", Telefono=611223344, Email="clara.santos@example.com"),
    Programador(id=8, DNI="87654321L", Nombre="Victor", Apellidos="Lopez Garcia", Telefono=633445566, Email="victor.lopez@example.com"),
    Programador(id=9, DNI="76543210M", Nombre="Elena", Apellidos="Gomez Fernandez", Telefono=622334411, Email="elena.gomez@example.com"),
    Programador(id=10, DNI="65432109N", Nombre="Raul", Apellidos="Mendez Torres", Telefono=688776655, Email="raul.mendez@example.com"),
]

#GET
@app.get("/programadores")
def get_programadores():
    return programadores_list



#En caso de que quiera un único programador:
@app.get("/programadores/{id_programadores}")              
def get_programador(id_programador : int):              
    return search_programador(id_programador)


@app.get("/programadores/")
def get_programador(id : int):
    return search_programador(id)


def search_programador(id : int):
    programadores = [programador for programador in programadores_list if programador.id == id]  

    if not programadores:
        raise HTTPException(status_code=404, detail="Programador no encontrado")
    return programadores[0]





#POST
@app.post("programadores", status_code=201, response_model=Programador)
def add_programador(programador : Programador):
    programador.id = next_id()
    programadores_list.append(programador)
    return programador



def next_id():
    return(max(programadores_list, key=id).id+1)




#PUT
@app.put("programadores/{id}")
def modify_programador(id:int, programador:Programador):
    for index, saved_programador in enumerate(programadores_list):
        if saved_programador.id == id:
            programador.id = id
            programadores_list[index] = programador
            return programador
    
    raise HTTPException(status_code=404, detail="Programador no encontrado")



#DELETE 
@app.delete("programadores/{id}")
def remove_programador(id : int):
    for saved_programador in programadores_list:
        if saved_programador == id:
            programadores_list.remove(saved_programador)
            return{}
    
    raise HTTPException(status_code=404, detail="Programador no encontrado")