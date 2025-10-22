from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class PaginaWeb(BaseModel):
    id: int
    Titulo: str
    Tematica : str
    URL : str
    IdProgramador: int


paginasWeb_list = [
    PaginaWeb(id=1, Titulo="Recetas Saludables Hoy", Tematica="Cocina / Salud", URL="https://www.recetassaludables.com", IdProgramador=101),
    PaginaWeb(id=2, Titulo="Viajes y Aventuras", Tematica="Turismo / Viajes", URL="https://www.viajeyaventuras.net", IdProgramador=102),
    PaginaWeb(id=3, Titulo="Programación para Todos", Tematica="Tecnología / Educación", URL="https://www.progparatodos.org", IdProgramador=103),
    PaginaWeb(id=4, Titulo="Mundo del Diseño Gráfico", Tematica="Diseño / Creatividad", URL="https://www.mundodiseno.com", IdProgramador=104),
    PaginaWeb(id=5, Titulo="Blog de Fotografía Urbana", Tematica="Fotografía / Arte", URL="https://www.fotourbana.blog", IdProgramador=105),
    PaginaWeb(id=6, Titulo="Finanzas Personales Fácil", Tematica="Finanzas / Educación", URL="https://www.finanzaspersonales.es", IdProgramador=106),
    PaginaWeb(id=7, Titulo="Salud Mental en Línea", Tematica="Psicología / Salud", URL="https://www.saludmentalenlinea.org", IdProgramador=107),
    PaginaWeb(id=8, Titulo="Podcast de Ciencia y Tecnología", Tematica="Ciencia / Tecnología", URL="https://www.cienciaytecnologia.fm", IdProgramador=108),
    PaginaWeb(id=9, Titulo="Gaming y eSports España", Tematica="Videojuegos / Entretenimiento", URL="https://www.gamingesports.es", IdProgramador=109),
    PaginaWeb(id=10, Titulo="Moda Sostenible Hoy", Tematica="Moda / Ecología", URL="https://www.modasostenible.com", IdProgramador=110)
]


#GET
@app.get("/paginas")
def paginas():
    return paginasWeb_list



@app.get("/paginas/{id_pagina}")
def get_pagina(id_pagina : int):
    return search_pagina(id_pagina)


@app.get("/paginas/")
def get_pagina(id : int):
    return search_pagina(id)



def search_pagina(id : int):
    paginas = [pagina for pagina in paginasWeb_list if pagina.id == id]

    if not paginas:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    return paginas[0]






#POST
@app.post("/paginas", status_code=201, response_model= PaginaWeb)
def add_pagina(pagina : PaginaWeb):
    pagina.id = next_id()
    paginasWeb_list.append(pagina)
    return pagina

def next_id():
    return(max(paginasWeb_list, key=id).id+1)



#PUT
@app.delete("/paginas/{id}")
def modify_pagina(id:int, pagina:PaginaWeb):
    for index, saved_pagina in enumerate(paginasWeb_list):
        if saved_pagina.id == id:
            pagina.id = id
            paginasWeb_list[index] = pagina
            return pagina

    raise HTTPException(status_code=404, detail="Página no encontrada")




#DELETE
@app.delete("/paginas/{id}")
def remove_pagina(id : int):
    for saved_pagina in paginasWeb_list:
        if saved_pagina.id == id:
            paginasWeb_list.remove(saved_pagina)
            return{}
    
    raise HTTPException(status_code=404, detail="Página no encontrada")