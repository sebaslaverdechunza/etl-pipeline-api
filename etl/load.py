# ------------------------------------------
# ¿Qué hace este archivo?
# Este módulo se encarga de cargar los DataFrames transformados
# en una base de datos relacional utilizando SQLAlchemy.
# Soporta SQLite (local) o PostgreSQL (nube, vía AWS RDS).
# ------------------------------------------

from sqlalchemy import create_engine # Para crear una conexión con la base de datos
from etl.config import get_database_url # Importa la función que retorna la URI según el motor configurado (.env)

def load_dataframes(df_products, df_purchases, df_purchase_products):
    """
    Carga los DataFrames transformados en la base de datos relacional
    (puede ser SQLite o PostgreSQL, según configuración en .env).
    """
    # Crear la conexión a la base de datos (engine puede ser SQLite o PostgreSQL)
    engine = create_engine(get_database_url())

    # Cargar cada DataFrame en su respectiva tabla.
    # Si la tabla ya existe, se reemplaza completamente.
    df_products.to_sql("products", engine, if_exists="replace", index=False)
    df_purchases.to_sql("purchases", engine, if_exists="replace", index=False)
    df_purchase_products.to_sql("purchase_products", engine, if_exists="replace", index=False)
    
    # Mensaje de confirmación en consola
    print("✅ Datos cargados correctamente en la base de datos")
