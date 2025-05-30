
import requests

def obtener_coordenadas_y_radio(api_key, direccion):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{direccion}, United States",
        "components": "country:US",
        "key": api_key
    }
    print(f"Consultando: {params['address']}")
    resp = requests.get(url, params=params).json()
    if resp.get("status") == "OK":
        resultado = resp["results"][0]
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
