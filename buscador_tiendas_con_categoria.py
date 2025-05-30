
import requests
import json
import time
import os

TIMEOUT = 10

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not GOOGLE_API_KEY:
    raise SystemExit("GOOGLE_API_KEY no definido en el entorno")

def obtener_categoria(place_id):
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&fields=types&key={GOOGLE_API_KEY}"
    )
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        datos = respuesta.json()
    except requests.RequestException:
        return "Categoría no encontrada"
    if datos.get('status') == 'OK' and 'result' in datos and 'types' in datos['result']:
        return datos['result']['types'][0]
    return "Categoría no encontrada"

def buscar_tiendas(ciudad, estado):
    query = f"rebar in {ciudad}, {estado}"
    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}&key={GOOGLE_API_KEY}"
    )
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        resultados = respuesta.json().get("results", [])
    except requests.RequestException:
        return []
    tiendas = []
    for r in resultados:
        nombre = r.get("name", "")
        direccion = r.get("formatted_address", "")
        place_id = r.get("place_id", "")
        telefono = "No disponible"  # Opcional: puedes agregar una llamada a place/details para extraerlo
        categoria = obtener_categoria(place_id)
        tiendas.append({
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "estado": estado,
            "teléfono": telefono,
            "categoría": categoria
        })
        time.sleep(1)  # Evitar límite de peticiones
    return tiendas

def guardar_resultados(tiendas, archivo="resultados.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            existentes = json.load(f)
    except FileNotFoundError:
        existentes = []
    existentes.extend(tiendas)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(existentes, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    ciudad = input("Ciudad: ").strip()
    estado = input("Estado (abreviado): ").strip().upper()
    resultados = buscar_tiendas(ciudad, estado)
    guardar_resultados(resultados)
    print(f"✅ {len(resultados)} tiendas guardadas con categoría.")
