# ¿Qué hace este DAG?
# Define un flujo de trabajo automático que ejecuta el pipeline ETL run_etl() todos los días. 
# Si ocurre un fallo, reintenta una vez después de 2 minutos y notifica por correo a juan_laverde1997@hotmail.com.




from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# Agrega dinámicamente la ruta raíz del proyecto (un nivel arriba de /dags)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run_pipeline import run_etl  # Importa la función principal del pipeline

# Configuración por defecto del DAG
default_args = {
    'owner': 'sebastian_laverde',
    'depends_on_past': False,
    'email': ['juan_laverde1997@hotmail.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Definición del DAG
with DAG(
    dag_id='etl_pipeline_ecommerce',
    default_args=default_args,
    description='Pipeline ETL desde API a PostgreSQL (Airflow)',
    schedule_interval='@daily',  # o usa '0 8 * * *' para 8AM
    start_date=datetime(2025, 7, 30),
    catchup=False,
    tags=['ETL', 'ecommerce'],
) as dag:

    ejecutar_etl = PythonOperator(
        task_id='ejecutar_pipeline',
        python_callable=run_etl,
    )

    ejecutar_etl
