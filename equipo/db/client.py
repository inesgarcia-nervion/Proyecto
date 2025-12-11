# Nos va a permitir conectarnos a nuestra base de datos.

from os import getenv
from pymongo import MongoClient


# Create a MongoClient using an explicit URI (default to local)
# You can override the URI by setting the environment variable MONGODB_URI
MONGO_URI = getenv("MONGODB_URI", "mongodb://localhost:27017")


# Base de datos en local
db_client = MongoClient("mongodb+srv://inesgarcia_db_user:<db_password>@cluster0.alqg98m.mongodb.net/?appName=Cluster0")

# Set sensible timeouts so connection attempts fail fast when MongoDB isn't available
# serverSelectionTimeoutMS controls how long the driver will try to find a server
# connectTimeoutMS controls how long a socket connect will wait
db_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000, connectTimeoutMS=20000)

# Example: to use a remote DB set MONGODB_URI='mongodb://user:pass@host:27017/dbname'