from fastapi import FastAPI


app = FastAPI()




@app.get("/users")
def inicio():
    return{"Hello": "World"}