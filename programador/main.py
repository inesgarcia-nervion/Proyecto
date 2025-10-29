from fastapi import FastAPI
from routers import paginas_web, programador
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(paginas_web.router)
app.include_router(programador.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def inicio():
    return {"Hello": "World"}