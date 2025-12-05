from routers import libros, autor, auth_users
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(libros.router)
app.include_router(autor.router)
app.include_router(auth_users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return {"Hello": "World"}