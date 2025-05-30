
import requests
from math import radians, sin, cos, sqrt, atan2

TIMEOUT = 10


def distancia_km(lat1, lon1, lat2, lon2):
    """Devuelve la distancia en kilómetros entre dos puntos."""
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def distancia_millas(lat1, lon1, lat2, lon2):
    """Devuelve la distancia en millas entre dos puntos."""
    return distancia_km(lat1, lon1, lat2, lon2) * 0.621371

def obtener_coordenadas_y_radio(api_key, direccion):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{direccion}, United States",
        "components": "country:US",
        "key": api_key
    }
    print(f"Consultando: {params['address']}")
    try:
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        data = resp.json()
    except requests.RequestException:
        return None, None, 5000

    if data.get("status") == "OK":
        resultado = data["results"][0]
        location = resultado["geometry"]["location"]
        bounds = resultado["geometry"].get("bounds")
        if bounds:
            ne = bounds["northeast"]
            sw = bounds["southwest"]
            radio = max(
                abs(ne["lat"] - sw["lat"]),
                abs(ne["lng"] - sw["lng"])
            ) * 111000 / 2
        else:
            radio = 5000
        return location["lat"], location["lng"], int(radio)
    return None, None, 5000
