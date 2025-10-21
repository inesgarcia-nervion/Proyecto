from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    id : int
    name : str
    surname : str
    age : int


users_list = [
    User(id= 1, name = "Inés", surname="García", age=24), 
    User(id= 2, name = "Ángela", surname="García", age=27),     
    User(id= 3, name = "Dylan", surname="Cano", age=25)
]

@app.get("/users")
def users():
    return users_list



@app.get("/users/{id_user}")              #El nombre nos lo podemos inventar
def get_user(id_user : int):              #El nombre tiene que ser igual al de arriba SIEMPRE
    users = search_user(id_user)
    return 
    
    
@app.get("/users/")       
def get_user(id_user : int):
    return search_user(id)


def search_user(id : int):        
    #  buscamos usuario por id en la lista
    # devuelve una lista vacía si no encuentra nada
    # devuelve una lista con el usuario encontrado
    users = [user for user in users_list if user.id == id]  #en user.id, el id hace referencia a la clase creada arriba
   
    # devolvemos la primera posición de la lista 
    
    if users:
        return users[0]
    raise HTTPException(status_code=404, detail="User not found")  
    # También se puede hacer: return users[0] if len(users) != 0 else {"error" : "User not found"}
    
