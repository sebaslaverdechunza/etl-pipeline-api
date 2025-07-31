# ------------------------------------------
# Este módulo toma los datos crudos extraídos desde la API REST
# y los transforma en tres DataFrames tabulares bien estructurados:
# - products
# - purchases (con total calculado)
# - purchase_products (tabla intermedia de relación)
# ------------------------------------------

import pandas as pd
from typing import List, Dict

def transform_products(json_data: dict) -> pd.DataFrame:
    """
    Transforma el JSON de productos en un DataFrame estructurado.
    """
    productos = json_data.get("data", []) # Extrae la lista bajo la clave 'data'
    df = pd.DataFrame(productos)          # Convierte la lista en un DataFrame

    # Renombrar y formatear

    # Renombra el campo 'createdAt' → 'created_at'
    df.rename(columns={"createdAt": "created_at"}, inplace=True)

    # Convierte 'created_at' a formato de fecha
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Devuelve solo las columnas relevantes
    return df[["id", "name", "description", "price", "category", "created_at"]]


def transform_purchases(data: List[Dict], products_map: Dict[int, float]) -> pd.DataFrame:
    """
    Transforma la lista de compras y calcula el total por compra,
    aplicando descuentos sobre los precios.
    """
    records = []
    for compra in data:
        productos = compra.get("products", [])
        total = 0

        # Calcular el total aplicando descuentos
        for p in productos:
            product_id = p.get("id")
            discount = p.get("discount", 0)
            price = products_map.get(product_id, 0) # Busca el precio del producto
            total += price * (1 - discount / 100) # Aplica el descuento
        
        # Construye el registro de compra
        records.append({
            "id": compra.get("id"),
            "status": compra.get("status"),
            "credit_card_type": compra.get("creditCardType", ""),
            "purchase_date": compra.get("purchaseDate"),
            "total": round(total, 2)
        })
    # Convierte la lista de compras en un DataFrame
    df = pd.DataFrame(records)
    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
    return df


def transform_purchase_products(data: List[Dict]) -> pd.DataFrame:
    """
    Genera la tabla intermedia entre compras y productos,
    agrupando por descuento y cantidad.
    """
    records = []
    for compra in data:
        productos = compra.get("products", [])
        contador = {}

        # Cuenta cuántas veces se repite cada producto por compra
        for producto in productos:
            pid = producto.get("id")
            discount = producto.get("discount", 0)
            key = (compra.get("id"), pid, discount)
            contador[key] = contador.get(key, 0) + 1

        # Construye los registros de la tabla intermedia
        for (purchase_id, product_id, discount), quantity in contador.items():
            records.append({
                "purchase_id": purchase_id,
                "product_id": product_id,
                "discount": discount,
                "quantity": quantity
            })

    return pd.DataFrame(records)
