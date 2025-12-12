def alumno_schema(alumno) -> dict:
    return {
        "id": str(alumno["_id"]),
        "Nombre": alumno["Nombre"],
        "Apellidos": alumno["Apellidos"],
        "Fecha_Nacimiento": alumno["Fecha_Nacimiento"],
        "Curso": alumno["Curso"],
        "Repetidor": alumno["Repetidor"],
        "Id_Colegio": alumno["Id_Colegio"]
    }

def alumnos_schema(alumnos) -> list:
    return [alumno_schema(alumno) for alumno in alumnos]

