
import requests
import time

def buscar_lugares(api_key, lat, lng, radio, keyword, buscar_telefono):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radio,
        "keyword": keyword,
        "key": api_key
    }
    resp = requests.get(url, params=params).json()
    resultados = []
    for lugar in resp.get("results", []):
        tienda = lugar.copy()
        tienda["telefono"] = "No disponible"
        tienda["categoria"] = "No especificada"

        if "place_id" in lugar:
            telefono, categoria = obtener_detalles(api_key, lugar["place_id"])
            if telefono:
                tienda["telefono"] = telefono
            if categoria:
                tienda["categoria"] = categoria

            if buscar_telefono:
                time.sleep(1)

        resultados.append(tienda)
    return resultados

def obtener_detalles(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,types",
        "key": api_key
    }
    resp = requests.get(url, params=params).json()
    telefono = "No disponible"
    categoria = "No especificada"

    if resp.get("status") == "OK" and "result" in resp:
        result = resp["result"]
        if "formatted_phone_number" in result:
            telefono = result["formatted_phone_number"]
        if "types" in result and isinstance(result["types"], list) and result["types"]:
            categoria = result["types"][0].replace("_", " ").title()

    return telefono, categoria
