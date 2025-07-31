
# ---------------------------------------------------------
# Este script es el punto de entrada principal del proceso ETL.
# Ejecuta las tres fases: Extracción, Transformación y Carga.
# 
# 1.  Carga configuraciones sensibles desde el archivo `.env`
# 2.  Extrae datos desde la API REST (productos y compras)
# 3.  Transforma los datos en estructuras limpias y tabulares
# 4.  Carga los datos en una base de datos relacional (SQLite o PostgreSQL)
# 
# Es completamente compatible con AWS RDS (PostgreSQL) y SQLite local.
# Se puede ejecutar directamente o integrarse en un DAG de Airflow.
# ---------------------------------------------------------

import os
import json
from dotenv import load_dotenv # Carga las variables de entorno desde el archivo `.env`

from etl.extract import fetch_from_api # Importa la función para consultar los endpoints de la API

from etl.transform import transform_products, transform_purchases, transform_purchase_products # Importa las funciones de transformación para estructurar los datos

from etl.load import load_dataframes # Importa la función para cargar los DataFrames a la base de datos

from etl.config import DB_ENGINE # Importa el motor actual de base de datos (sqlite o postgresql)

from datetime import datetime

def run_etl():
    # Ejecuta el pipeline completo, mostrando mensajes y controlando errores
    print("📦 Iniciando proceso ETL -", datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Muestra timestamp del inicio

    try:
        # === Cargar variables de entorno ===
        load_dotenv() # Carga credenciales desde .env
        TOKEN = os.getenv("API_TOKEN")
        DB_URI = os.getenv("DB_URI")

        print("🔍 API_TOKEN:", TOKEN)
        print("🔍 DB_URI:", DB_URI)
        print(f"🛢️ Motor de base de datos activo: {DB_ENGINE.upper()}")

        if DB_ENGINE == "sqlite":
            print("📂 Cargando datos en archivo local: etl_project.db")
        elif DB_ENGINE == "postgresql":
            print("☁️ Cargando datos en AWS RDS (PostgreSQL)")

        if not TOKEN or not DB_URI:
            raise ValueError("❌ API_TOKEN o DB_URI no están definidos en el archivo .env.")

        # === Endpoints ===
        URL_PRODUCTOS = "https://mnpwhdbcsk.us-east-2.awsapprunner.com/api/products"
        URL_COMPRAS = "https://mnpwhdbcsk.us-east-2.awsapprunner.com/api/purchases"

        print("🔍 Extrayendo datos desde la API...")
        productos_raw = fetch_from_api(URL_PRODUCTOS, TOKEN)
        compras_raw = fetch_from_api(URL_COMPRAS, TOKEN)
        # Llama a la API REST y obtiene los datos

        print(f"📦 Tipo productos_raw: {type(productos_raw)}")
        print(f"📦 Tipo compras_raw: {type(compras_raw)}")
        print(f"🧾 Ejemplo de compra:\n{json.dumps(compras_raw.get('data', [])[:2], indent=2)}")

        print("🧼 Transformando datos...")
        df_products = transform_products(productos_raw)

        products_map = {row["id"]: row["price"] for row in productos_raw["data"]}
        df_purchases = transform_purchases(compras_raw["data"], products_map)
        df_purchase_products = transform_purchase_products(compras_raw["data"])
        # Estructura y limpia los datos

        print("💾 Cargando datos a la base de datos...")
        load_dataframes(df_products, df_purchases, df_purchase_products) # Inserta los resultados en base de datos
        

        print("✅ ETL ejecutado correctamente.")

    except Exception as e:
        print(f"❌ Error en el proceso ETL: {e}")

if __name__ == "__main__":
    run_etl()

