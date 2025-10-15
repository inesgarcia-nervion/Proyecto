from fastapi import FastAPI
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
    users = [user for user in users_list if user.id == id_user]  #en user.id, el id hace referencia a la clase creada arriba
    
    
    return users[0] if users else {"error" : "User not found"}    #Si la longitud de la lista es distinta a 0
    # También se puede hacer: return users[0] if len(users) != 0 else {"error" : "User not found"}