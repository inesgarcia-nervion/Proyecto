from pymongo import MongoClient


# Nos creamos un objeto de tipo MongoClient
# Al crear el objeto ya establecemos una conexión con la base de datos
# No le indicamos ningún parámetro al constructor porque vamos a conectar con la base de datos local por defecto
# Si la base de datos estuviese en un servidor si que tendríamos que indicarle la URL del servidor


# Base de datos en local
db_client = MongoClient("mongodb+srv://inesgarcia_db_user:<db_password>@cluster0.alqg98m.mongodb.net/?appName=Cluster0")


# Base de datos en remoto
# db_client = MongoClient()