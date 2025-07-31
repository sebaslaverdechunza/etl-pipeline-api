# ----------------------------------------
# ¿Qué hace este archivo?
# Configura las variables necesarias para el pipeline ETL.
# Centraliza:
#   1. Autenticación para la API externa.
#   2. URLs de los endpoints de productos y compras.
#   3. Configuración del motor de base de datos (SQLite o PostgreSQL).
# ----------------------------------------

import os
from dotenv import load_dotenv # Para cargar las variables definidas en el archivo .env

# Cargar variables desde el archivo .env
load_dotenv()

# -----------------------------
# 📡 API - Endpoints y token
# -----------------------------

# Definición base de la URL del API
BASE_URL = "https://mnpwhdbcsk.us-east-2.awsapprunner.com"
# Endpoints específicos para productos y compras
URL_PRODUCTOS = f"{BASE_URL}/api/products"
URL_COMPRAS = f"{BASE_URL}/api/purchases"

# Token de autenticación para el header x-api-key
TOKEN = os.getenv("API_TOKEN")
if not TOKEN:
    raise ValueError("⚠️ No se encontró la variable API_TOKEN en el archivo .env.")

# -----------------------------
# 🛢️ Conexión a base de datos
# -----------------------------
# Tipo de motor de base de datos: sqlite o postgresql (por defecto sqlite)
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()  # por defecto sqlite
# URI de conexión que se usará si el motor es PostgreSQL
DB_URI = os.getenv("DB_URI")

# Modo SQLite (por defecto)

# Ruta del archivo .db local (SQLite)
SQLITE_PATH = "etl_project.db"
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

# Verificar la conexión adecuada según motor
def get_database_url():
    """
    Devuelve la URL de conexión a la base de datos dependiendo del motor seleccionado.
    Si es PostgreSQL y no se especificó DB_URI, lanza un error.
    """
    if DB_ENGINE == "postgresql":
        if not DB_URI:
            raise ValueError("⚠️ No se encontró DB_URI en el archivo .env para PostgreSQL.")
        return DB_URI
    return SQLITE_URL