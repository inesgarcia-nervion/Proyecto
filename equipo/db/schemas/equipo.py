def equipo_schema(equipo) -> dict:
    # El id en base de datos es _id, pero en la API lo queremos como id
    return {
        "id": str(equipo["_id"]),
        "Nombre": equipo["Nombre"],
        "Ciudad": equipo["Ciudad"],
        "AñoFundación": equipo["AñoFundación"],
        "Estadio": equipo["Estadio"]
    }

def equipos_schema(equipos) -> list:
    return [equipo_schema(equipo) for equipo in equipos]