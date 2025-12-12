def colegio_schema(colegio) -> dict:
    return {
        "id": str(colegio["_id"]),
        "Nombre": colegio["Nombre"],
        "Distrito": colegio["Distrito"],
        "Tipo": colegio["Tipo"],
        "Direccion": colegio["Direccion"]
    }

def colegios_schema(colegios) -> list:
    return [colegio_schema(colegio) for colegio in colegios]
