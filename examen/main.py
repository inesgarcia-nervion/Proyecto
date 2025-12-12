from routers import alumnos, colegios, auth_users
from fastapi import FastAPI


app = FastAPI()

app.include_router(alumnos.router)
app.include_router(colegios.router)
app.include_router(auth_users.router)


@app.get("/")
def inicio():
    return {"Hello" : "World"}