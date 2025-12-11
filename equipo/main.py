#pip install "fastapi[standard]"
# autenticacion con JWT: pip install pyjwt
# Para hashing de contraseñas:  pip install "pwdlib[argon2]"
# Base de datos MongoDB: pip install pymongo

from routers import equipo, jugadores, auth_users, jugadores_db, equipos_db
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(equipo.router)
app.include_router(jugadores.router)
app.include_router(auth_users.router)
app.include_router(jugadores_db.router)
app.include_router(equipos_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return {"Hello": "World"}
