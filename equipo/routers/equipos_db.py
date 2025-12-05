from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .auth_users import authentication
from db.models.equipo import Equipo
from db.client import db_client 
from db.schemas.equipo import equipo_schema, equipos_schema

from bson import ObjectId

router = APIRouter(prefix="/equiposdb", tags=["equiposdb"])

# la siguiente lista pretende simular una base de datos para probar nuestra API
equipos_list = []



# ============================================================
# GET → devuelve todos los registros
# ============================================================
@router.get("/", response_model=list[Equipo])
async def equipos():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return equipos_schema(db_client.test.equipos.find())



# ============================================================
# GET tipo query → busca por id
# http://127.0.0.1:8000/equiposdb?id=xxxx
# ============================================================
@router.get("", response_model=Equipo)
async def equipo(id: str):
    return search_equipo_id(id)




# ============================================================
# GET por id
# ============================================================
@router.get("/{id}", response_model=Equipo)
async def equipo(id: str):
    return search_equipo_id(id)



# ============================================================
# POST → añade equipo a la base de datos
# ============================================================
@router.post("/", response_model=Equipo, status_code=201)
async def add_equipo(equipo: Equipo):
    #print("dentro de post")
    if type(search_equipo(equipo.Nombre, equipo.Ciudad)) == Equipo:
        raise HTTPException(status_code=409, detail="Equipo already exists")
    
    equipo_dict = equipo.model_dump()
    del equipo_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.equipos.insert_one(equipo_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    equipo_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Equipo(**equipo_dict)
    
    
    
# ============================================================
# PUT → modificar equipo existente
# ============================================================
@router.put("/{id}", response_model=Equipo)
async def modify_equipo(id: str, new_equipo: Equipo):
    # Convertimos el usuario a un diccionario
    equipo_dict = new_equipo.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del equipo_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.equipos.find_one_and_replace({"_id":ObjectId(id)}, equipo_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_equipo_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Equipo not found")
    


# ============================================================
# DELETE → eliminar equipo
# ============================================================
@router.delete("/{id}", response_model=Equipo)
async def delete_equipo(id:str):
    found = db_client.test.equipos.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Equipo not found")
    return Equipo(**equipo_schema(found))




# ============================================================
# Funciones auxiliares
# ============================================================
# El id de la base de datos es un string, ya no es un entero
def search_equipo_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        equipo = equipo_schema(db_client.test.equipos.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Equipo(**equipo)
    except:
        return {"error": "Equipo not found"}



def search_equipo(name: str, surname: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        equipo = equipo_schema(db_client.test.equipos.find_one({"Nombre":name, "Ciudad":surname}))
        return Equipo(**equipo)
    except:
        return {"error": "Equipo not found"}


def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(equipo.id for equipo in equipos_list))+1