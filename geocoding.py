
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIMEOUT = 10

def obtener_coordenadas_y_radio(api_key, direccion):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{direccion}, United States",
        "components": "country:US",
        "key": api_key
    }
    logger.info(f"Consultando: {params['address']}")
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
