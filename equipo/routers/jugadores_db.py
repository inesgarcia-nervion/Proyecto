from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .auth_users import authentication
from db.models.jugador import Jugadores
from db.client import db_client 
from db.schemas.jugador import jugador_schema, jugadores_schema

from bson import ObjectId

router = APIRouter(prefix="/jugadoresdb", tags=["jugadoresdb"])

# la siguiente lista pretende simular una base de datos para probar nuestra API
jugadores_list = []



# ============================================================
# GET → devuelve todos los registros
# ============================================================
@router.get("/", response_model=list[Jugadores])
async def jugadores():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return jugadores_schema(db_client.test.jugadores.find())



# ============================================================
# GET tipo query → busca por id
# http://127.0.0.1:8000/jugadoresdb?id=xxxx
# ============================================================
@router.get("", response_model=Jugadores)
async def jugador(id: str):
    return search_jugador_id(id)




# ============================================================
# GET por id
# ============================================================
@router.get("/{id}", response_model=Jugadores)
async def jugador(id: str):
    return search_jugador_id(id)



# ============================================================
# POST → añade jugador a la base de datos
# ============================================================
@router.post("/", response_model=Jugadores, status_code=201)
async def add_jugador(jugador: Jugadores):
    #print("dentro de post")
    if type(search_jugador(jugador.Nombre, jugador.Edad)) == Jugadores:
        raise HTTPException(status_code=409, detail="Jugador already exists")
    
    jugador_dict = jugador.model_dump()
    del jugador_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.jugadores.insert_one(jugador_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    jugador_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Jugadores(**jugador_dict)
    
    
    
# ============================================================
# PUT → modificar jugador existente
# ============================================================
@router.put("/{id}", response_model=Jugadores)
async def modify_jugador(id: str, new_jugador: Jugadores):
    # Convertimos el usuario a un diccionario
    jugador_dict = new_jugador.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del jugador_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.jugadores.find_one_and_replace({"_id":ObjectId(id)}, jugador_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_jugador_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Jugador not found")
    


# ============================================================
# DELETE → eliminar jugador
# ============================================================
@router.delete("/{id}", response_model=Jugadores)
async def delete_jugador(id:str):
    found = db_client.test.jugadores.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Jugador not found")
    return Jugadores(**jugador_schema(found))




# ============================================================
# Funciones auxiliares
# ============================================================
# El id de la base de datos es un string, ya no es un entero
def search_jugador_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        jugador = jugador_schema(db_client.test.jugadores.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Jugadores(**jugador)
    except:
        return {"error": "Jugador not found"}



def search_jugador(name: str, surname: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        jugador = jugador_schema(db_client.test.jugadores.find_one({"name":name, "surname":surname}))
        return Jugadores(**jugador)
    except:
        return {"error": "Jugador not found"}


def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(jugador.id for jugador in jugadores_list))+1