from routers import equipo, jugadores, auth_users
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(equipo.router)
app.include_router(jugadores.router)
app.include_router(auth_users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return {"Hello": "World"}
