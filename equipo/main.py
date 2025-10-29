from fastapi import FastAPI
from routers import equipo, jugadores
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Routers
app.include_router(equipo.router)
app.include_router(jugadores.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return {"Hello": "World"}