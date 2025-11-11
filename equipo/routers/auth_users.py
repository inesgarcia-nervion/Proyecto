from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from datetime import *
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



# Clave que se reutilizará como semilla para generar el token
# openssl rand -hex 32 (abrir terminal tipo git bash para generar una clave segura)
SECRET_KEY = "b3a9e1c1bfbf86fb374ca4204b927d4329e52760d74e813956c67d49819c804c"  # Para el token
# Algoritmo para cifrar el tokem

# Definimos el algoritmo de encriptacion
ALGORITHM = "HS256"     # Para el token

# Duracion del token
ACCESS_TOKEN_EXPIRE_MINUTES = 5   # Para el token



#Objecto que se utilizará para el cálculo del hash y 
# y la verificación de las contraseñas
password_hash = PasswordHash.recommended()   # Para la contraseña

outh2 = OAuth2PasswordBearer(tokenUrl="login")   # Para el token


router = APIRouter()

class User(BaseModel):
    username: str
    fullname: str
    email : str
    disabled : bool         #Si la cuenta esta deshabilitada o no


class UserDB(User):
    password : str
   

# Base de datos (tenemos que copiar aquí los usuarios porque necesitamos los hush (la contraseña))
users_db = {
    "inesgc": {
        "username": "inesgc",
        "fullname": "Ines Garcia",
        "email": "inesgc@prueba.es",
        "disabled": False,
        "password": "123456"
    },
    "prueba" : {
        "username": "prueba",
        "fullname": "Prueba Prueba",
        "email": "prueba@prueba.es",
        "disabled": False,
        "password": "123456"
    }
    
}



# Como será el registro de nuestros usuarios
@router.post("/register", status_code=201)
def register(user : UserDB): # UsuarioDB porque queremos la contraseña
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password # Sustituimos la contraseña por la encriptada (la nueva)
        users_db[user.username] = user
        return user
    raise HTTPException(status_code=409, detail="User already exists")
    


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if user:    # Si no está en blanco
        # Si el usuario no existe en la base de datos
        # Comprobamos las contraseñas
        if password_hash.verify(form.password, user["password"]):
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = {"sub": user.username, "exp":expire}
            # Generamos el token
            token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token":token, "token_type":"bearer"}
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    