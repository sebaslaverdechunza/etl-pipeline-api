# Proyecto ETL: Consumo y carga de datos en Data Warehouse relacional

Este proyecto consiste en la construcción de un pipeline ETL para integrar datos provenientes de una API REST hacia un Data Warehouse relacional.

---
> **Nota importante**  
> Este proyecto fue desarrollado como parte de un reto técnico para el proceso de selección de **Windmar Home**.  

> La solución presentada no representa una implementación oficial.

> Todos los nombres, endpoints o elementos gráficos utilizados tienen únicamente fines académicos o demostrativos.

--
### Estructura de Carpeta 
```text
ETL_PROJECT/
│
├── etl/                      # Módulos del proceso ETL
│   ├── __init__.py
│   ├── config.py             # Configuración global (DB, API)
│   ├── extract.py            # Extracción de datos desde la API
│   ├── transform.py          # Transformación de datos en DataFrames
│   └── load.py               # Carga de datos a la base de datos
│
├── tests/
│   └── test_transform.py     # Tests unitarios para la capa de transformación
│
├── run_pipeline.py           # Script principal para ejecutar el flujo ETL
├── requirements.txt          # Dependencias del proyecto
├── .env                      # Variables de entorno (token, conexión BD)
├── README.md                 # Documentación del proyecto
├── etl_project.db            # Base de datos SQLite (si se usa localmente)
└── Capturas de pantalla del pipeline  # Evidencia visual del funcionamiento
```



## 📌 Descripción del proyecto
Este proyecto implementa un pipeline ETL (Extract, Transform, Load) en Python que:

- 🔍 Extrae datos desde una API REST protegida con token (`x-api-key`).
- 🧼 Transforma la información en tres tablas relacionales:
	  - `products`
	  - `purchases`
	  - `purchase_products`
- 💾 Carga los datos transformados en una base de datos relacional, con soporte para:
	  - SQLite (modo local)
	  - PostgreSQL (modo nube - AWS RDS) --- Interfaz gráficca pgAdmin
--
> El objetivo es construir un proceso modular, confiable y automatizado que pueda integrarse fácilmente a un entorno de producción o a un Data Warehouse corporativo.

---

## Instrucciones de ejecución
Este proyecto puede ejecutarse de forma manual desde la terminal o, opcionalmente, con Apache Airflow (DAG incluido pero no ejecutado por compatibilidad con Python 3.13).

	1.  Clonar el repositorio

git clone https://github.com/tu-usuario/etl-project.git
cd etl-project

	2. Crear entorno virtual (opcional, recomendado)
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac

	3. Instalar dependencias

pip install -r requirements.txt

	4. Configurar variables de entorno
Edita el archivo .env:

	API_TOKEN=tu_token_aqui
	DB_ENGINE=postgresql
	DB_URI=postgresql://usuario:contraseña@host:5432/nombre_base_datos

>También puedes usar SQLite para pruebas:

DB_ENGINE=sqlite
DB_URI=sqlite:///etl_project.db

	 5. Ejecutar el pipeline ETL manualmente
python run_pipeline.py

Por ejemplo: PS C:\Users\USUARIO\Documents\ETL_PROJECT> python run_pipeline.py

#### Esto realizará:

- Extracción de productos y compras desde la API
- Transformación en tres tablas limpias
- Carga de datos en PostgreSQL (o SQLite)


	6. Ejecutar pruebas

pytest tests/

>Esto validará que las transformaciones clave están funcionando correctamente.

	7. (Opcional) Ejecutar con Airflow

>El DAG etl_pipeline_dag.py está incluido, pero no fue ejecutado localmente por incompatibilidad con Python 3.13.

En entornos compatibles (Python 3.11 o Docker):

	airflow db init
	airflow scheduler
	airflow webserver


Luego, activa el DAG desde la interfaz web o con:

	airflow dags trigger etl_pipeline_ecommerce

##  Stack tecnológico usado

| Herramienta        | Rol dentro del proyecto                            |
|--------------------|----------------------------------------------------|
| **Python **       | Lenguaje base para el desarrollo del pipeline      |
| `pandas`           | Transformación y manipulación de datos tabulares  |
| `requests`         | Llamadas HTTP a la API REST                        |
| `sqlalchemy`       | Conexión y escritura a bases de datos relacionales|
| `tenacity`         | Reintentos automáticos en caso de fallas HTTP     |
| `python-dotenv`    | Lectura segura de variables de entorno             |
| `psycopg2-binary`  | Driver PostgreSQL para SQLAlchemy                  |
| `pytest`           | Validación unitaria de funciones de transformación|
| `pgAdmin 4`        | Exploración visual del Data Warehouse en la nube  |

### Stack no implementado y justificación

Aunque el reto recomendaba considerar herramientas adicionales como Spark, Airflow, AWS Glue o tecnologías de streaming, estas no fueron implementadas por las siguientes razones:

| Tecnología                | Motivo de no implementación                                           |
|---------------------------|------------------------------------------------------------------------|
| **Apache Spark**          | No se requirió procesamiento distribuido; el volumen de datos es bajo y Pandas fue suficiente. |
| **Apache Airflow**        | Se implementó un DAG funcional (`etl_pipeline_dag.py`), pero no se ejecutó debido a que Apache Airflow aún no es compatible con Python 3.13. Se documentó el uso y está listo para producción. |
| **AWS Glue**              | No fue necesario un entorno serverless para ETL, pero el proyecto fue diseñado modularmente y es compatible con una futura migración a Glue. Se documentó esta posibilidad en el README. |
| **Kafka / Flink / Kinesis** | No se trató de un caso de procesamiento en tiempo real (streaming), sino de una carga batch desde una API REST. |

 >*A pesar de no usarlas, el proyecto fue estructurado para facilitar su futura adopción si el contexto lo amerita.*

---

## Scripts SQL para crear las tablas destino
A continuación se presentan las sentencias CREATE TABLE correspondientes a cada una de las tres tablas generadas en el proceso ETL:

-- Tabla de productos
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    price NUMERIC,
    category TEXT,
    created_at TIMESTAMP
);

- id: Identificador único del producto.
- name: Nombre del producto.
- description: Descripción breve.
- price: Precio unitario.
- category: Categoría del producto.
- created_at: Fecha de creación del producto.


 >Uso: Esta tabla se alimenta con los datos provenientes del endpoint /api/products.

-- Tabla de compras
CREATE TABLE purchases (
    id TEXT PRIMARY KEY,
    status TEXT,
    credit_card_type TEXT,
    purchase_date TIMESTAMP,
    total NUMERIC
);

- id: ID único de la compra.
- status: Estado de la compra (ej. completed, cancelled).
- credit_card_type: Tipo de tarjeta usada.
- purchase_date: Fecha de la compra.
- total: Valor total pagado (incluyendo descuentos).



 >Uso: Esta tabla se llena usando los datos de /api/purchases, después de transformarlos y calcular el total de la compra.

-- Tabla de relación entre compras y productos
CREATE TABLE purchase_products (
    purchase_id TEXT,
    product_id INTEGER,
    discount NUMERIC,
    quantity INTEGER,
    PRIMARY KEY (purchase_id, product_id, discount),
    FOREIGN KEY (purchase_id) REFERENCES purchases(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

- purchase_id: ID de la compra.
- product_id: ID del producto comprado.
- discount: Descuento aplicado a ese producto.
- quantity: Cantidad de veces que ese producto aparece en la compra.

>Uso: Esta tabla permite analizar qué productos se compraron en cada compra, con qué descuento y en qué cantidad.

## 📌 Resultado final del ETL

Tras la ejecución del pipeline, se cargaron exitosamente los siguientes volúmenes de datos en el Data Warehouse relacional:

| Tabla               | Registros cargados |
| ------------------- | ------------------ |
| `products`          |2.157 productos    |
| `purchases`         |3.534 compras    |
| `purchase_products` |18.119 relaciones |
| `Total` | 23.810 registros |

## Diagrama del flujo ETL o arquitectura.

[![Diagrama de Flujo ETL ](https://drive.google.com/file/d/19V1eiy__PIGx5AwojQL2ZnXtUy_yrPOc/view?usp=drive_link "Diagrama de Flujo ETL ")](https://drive.google.com/file/d/19V1eiy__PIGx5AwojQL2ZnXtUy_yrPOc/view?usp=drive_link "Diagrama de Flujo ETL ")

[Realizar Diagramas de flujo](https://www.mermaidchart.com/app/projects/c6c29f9c-9958-4e79-a071-424332ed4d36/diagrams/34c6449c-c4f9-4062-82d1-8c4350341420/version/v0.1/edit "Realizar Diagramas de flujo")
