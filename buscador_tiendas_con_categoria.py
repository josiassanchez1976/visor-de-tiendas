
import requests
import json
import time

GOOGLE_API_KEY = "TU_API_KEY"  # ← Reemplaza con tu clave real

def obtener_categoria(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=types&key={GOOGLE_API_KEY}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if 'result' in datos and 'types' in datos['result']:
        return datos['result']['types'][0]  # Categoría principal
    return "Categoría no encontrada"

def buscar_tiendas(ciudad, estado):
    query = f"rebar in {ciudad}, {estado}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}"
    respuesta = requests.get(url)
    resultados = respuesta.json().get("results", [])
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
