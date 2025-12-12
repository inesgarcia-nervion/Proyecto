from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from jwt import PyJWKError
from datetime import *


#Clave generada con Git Bash (Comando: openssl rand -hex 32)
SECRET_KEY = "e3bf97286956702583fdadc597e5537868c2583bcdd7250289ac9366a062e6a4"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 5 #5 minutos de fecha de expiracion


password_hash = PasswordHash.recommended()
outh2 = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

class User(BaseModel):
    username: str
    fullname: str
    disabled : bool
    
class UserDB(User):
    password : str
    
    
users_db = {
    "inesgc": {
        "username" : "inesgc",
        "fullname" : "Ines Garcia",
        "disabled" : False,
        "password" : "1234"
    }
}

@router.post("/auth/registro", status_code=201)
def register(user : UserDB):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user.model_dump()
        return user
    raise HTTPException(status_code=409, detail="El usuario ya existe")


@router.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if users_db:
        user = UserDB(**user_db)
        try: 
            if password_hash.verify(form.password, user.password):
                expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = {"sub": user.username, "exp": expire}
                token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
                return {"access_token": token,"token_type":"bearer"}
        except:
            raise HTTPException(status_code=400, detail="Error en la autenticación")
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    

async def authentication(token : str = Depends(outh2)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales de autentificación inválidas", headers={"WWW-Authenticate" : "Bearer"})
    except PyJWKError:
        raise HTTPException(status_code=401, detail="Credenciales de autentificación inválidas", 
                                headers={"WWW-Autheticate" : "Bearer"})
    
    user = User(**users_db[username])
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user