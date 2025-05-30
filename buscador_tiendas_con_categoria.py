import os
import json
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY", "")
TIMEOUT = 10

if not API_KEY:
    raise SystemExit("GOOGLE_API_KEY no definido")

async def obtener_categoria(session, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "types", "key": API_KEY}
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return "Categoría no encontrada"
        data = await resp.json()
    if "result" in data and "types" in data["result"]:
        return data["result"]["types"][0]
    return "Categoría no encontrada"

async def buscar_tiendas_async(ciudad, estado):
    query = f"rebar in {ciudad}, {estado}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": API_KEY}
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return []
            resultados = (await resp.json()).get("results", [])
        tareas = []
        tiendas = []
        for r in resultados:
            nombre = r.get("name", "")
            direccion = r.get("formatted_address", "")
            place_id = r.get("place_id", "")
            tiendas.append({
                "nombre": nombre,
                "direccion": direccion,
                "ciudad": ciudad,
                "estado": estado,
                "teléfono": "No disponible",
                "categoría": ""
            })
            tareas.append(obtener_categoria(session, place_id))
        cats = await asyncio.gather(*tareas, return_exceptions=True)
        for tienda, cat in zip(tiendas, cats):
            tienda["categoría"] = cat if isinstance(cat, str) else "Categoría no encontrada"
        return tiendas

def buscar_tiendas(ciudad, estado):
    return asyncio.run(buscar_tiendas_async(ciudad, estado))


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
