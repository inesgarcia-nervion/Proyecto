from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #Esta librería me va a permitir crear clases para mi API pero de forma mucho más sencilla.


app = FastAPI()

# Definimos la clase User
class User(BaseModel):
    id : int
    name : str
    surname : str
    age : int


# Creamos una lista de usuarios (simulando una base de datos)
users_list = [
    User(id= 1, name = "Inés", surname="García", age=24), 
    User(id= 2, name = "Ángela", surname="García", age=27),     
    User(id= 3, name = "Dylan", surname="Cano", age=25)
]


#GET: Buscar usuarios de la API
@app.get("/users")
def users():
    return users_list



@app.get("/users/{id_user}")              #El nombre nos lo podemos inventar
def get_user(id_user : int):              #El nombre tiene que ser igual al de arriba SIEMPRE
    return search_user(id_user)

    
    
@app.get("/users/")       
def get_user(id : int):
    return search_user(id)



def search_user(id : int):        
    # Buscamos usuario por id en la lista
    # Devuelve una lista vacía si no encuentra nada
    # Devuelve una lista con el usuario encontrado
    users = [user for user in users_list if user.id == id]  #en user.id, el id hace referencia a la clase creada arriba

    # devolvemos la primera posición de la lista si existe
    if not users:
        raise HTTPException(status_code=404, detail="User not found")      # También se puede hacer: return users[0] if len(users) != 0 else {"error" : "User not found"}
    return users[0]







#POST: Añadir nueva información
@app.post("/users", status_code=201, response_model=User)
def add_user(user : User):          #definimos un usuario en nuestra lista
    # Calculamos el siguiente id y se lo 
    # machacamos al usuario recibido por parámetro
    user.id = next_id()

    # Añadimos el usuario de la lista
    users_list.append(user)

    # Devolvemos al usuario añadido
    return user



def next_id():
    return(max(users_list, key=id).id+1)       # Devuelve usuario con mayor id y le suma 1




#PUT: Modificar la información
@app.put("/users/{id}") # Le tengo que pasar un id para que funcione
def modify_user(id:int, user:User):
    # El método enumerate devuelve el indice de la lista
    # y el usuario almacenado en dicho indice
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            user.id = id
            users_list[index] = user
            return user
        
    raise HTTPException(status_code=404, detail="User not found")           # Si no encuentra nada en el bucle, lanza excepción



#DELETE: Eliminar un recurso 
@app.delete("/users/{id}")
def remove_user(id : int):
    for saved_user in users_list:
        if saved_user.id == id:
            users_list.remove(saved_user)
            return{}
    
    raise HTTPException(status_code=404, detail="User not found")


