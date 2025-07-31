# ----------------------------------------------
# Este módulo contiene pruebas unitarias para validar
# la lógica de transformación del pipeline ETL.
# Usa `pytest` y datos simulados para probar:
# - Cálculo del total por compra con descuento
# - Conteo correcto de productos por compra
# ----------------------------------------------

# Paso necesario para permitir importar desde la carpeta padre (etl/)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Librerías requeridas
import pytest
from etl.transform import transform_purchases, transform_purchase_products

@pytest.fixture
def dummy_data():
    """
    Devuelve una lista de compras simuladas para probar la lógica ETL.
    Contiene:
    - Una compra con dos productos repetidos (id=101, descuento 10%)
    - Un tercer producto distinto (id=102, sin descuento)
    """
    return [
        {
            "id": "compra_1",
            "status": "completed",
            "creditCardType": "Visa",
            "purchaseDate": "2024-01-01",
            "products": [
                {"id": 101, "discount": 10},
                {"id": 101, "discount": 10},
                {"id": 102, "discount": 0}
            ]
        }
    ]

def test_transform_purchases(dummy_data):
    """
    Verifica que el total de la compra se calcule correctamente:
    - Producto 101 aparece dos veces con 10% descuento: 100 * 0.9 * 2 = 180
    - Producto 102 sin descuento: 200
    - Total esperado: 180 + 200 = 380
    """
    products_map = {101: 100, 102: 200} # Precios de referencia para los productos

    df = transform_purchases(dummy_data, products_map)

    assert df.loc[0, "id"] == "compra_1"
    assert df.loc[0, "status"] == "completed"
    assert df.loc[0, "credit_card_type"] == "Visa"
    assert df.loc[0, "total"] == pytest.approx(100 * 0.9 * 2 + 200)


def test_transform_purchase_products(dummy_data):
    """
    Verifica que el conteo de productos por compra funcione correctamente:
    - Producto 101 aparece 2 veces
    - Producto 102 aparece 1 vez
    """ 
    df = transform_purchase_products(dummy_data)
    # Validar que el producto 101 aparece dos veces
    row = df[(df["purchase_id"] == "compra_1") & (df["product_id"] == 101)]
    assert row.iloc[0]["quantity"] == 2
    # Validar que el producto 102 aparece una vez
    row2 = df[(df["purchase_id"] == "compra_1") & (df["product_id"] == 102)]
    assert row2.iloc[0]["quantity"] == 1