def jugador_schema(jugador) -> dict:
    # El id en base de datos es _id, pero en la API lo queremos como id
    return {
        "id": str(jugador["_id"]),
        "Nombre": jugador["Nombre"],
        "Edad": jugador["Edad"],
        "Posición": jugador["Posición"],
        "Nacionalidad": jugador["Nacionalidad"],
        "Salario": jugador["Salario"],
        "idEquipo": jugador["idEquipo"]
    }
    
    
def jugadores_schema(jugadores) -> list:
    return [jugador_schema(jugador) for jugador in jugadores]  