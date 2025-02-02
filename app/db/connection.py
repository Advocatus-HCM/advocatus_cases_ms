from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Crear cliente MongoDB (Motor)
client = AsyncIOMotorClient(MONGO_URI)

# Seleccionar la base de datos
database = client[DATABASE_NAME]

cases_collection = database["cases"]

# Exportar las variables
__all__ = ["database", "client", "cases_collection"]
