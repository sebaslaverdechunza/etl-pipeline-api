
# ------------------------------------------
# ¿Qué hace este archivo?
# Este módulo contiene la función que se encarga de extraer datos
# desde una API REST autenticada usando un header 'x-api-key'.
# Se usa la librería `requests` para las solicitudes HTTP
# y `tenacity` para manejar reintentos automáticos ante errores temporales.
# ------------------------------------------


import requests # Para hacer solicitudes HTTP a la API
from tenacity import retry, stop_after_attempt, wait_fixed  # Para manejar reintentos automáticos

# Decorador que reintenta la función hasta 3 veces si falla, esperando 2 segundos entre cada intento
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))

def fetch_from_api(url, api_key):
    """
    Realiza una solicitud GET a la API especificada en `url` usando el token `api_key`.

    Parámetros:
        url (str): Endpoint al que se desea hacer la solicitud.
        api_key (str): Clave API usada para autenticación en el header.

    Retorna:
        dict: La respuesta JSON de la API convertida a un diccionario de Python.
    """
    # Construcción del header de autenticación
    headers = {
        "x-api-key": api_key
    }
    print(f"📡 Llamando a: {url}") # Log de seguimiento para saber qué endpoint se está consumiendo
    
    # Realiza la solicitud GET con el header autenticado
    response = requests.get(url, headers=headers)

    # Si la respuesta no es exitosa, lanza una excepción personalizada con detalles
    if response.status_code != 200:
        raise Exception(f"Error al consultar {url} - Código: {response.status_code} - Respuesta: {response.text}")
    
    # Devuelve el cuerpo de la respuesta como JSON (estructura tipo dict)
    return response.json()  # ✅ Esta línea es clave
