
import asyncio
from typing import List

import aiohttp

TIMEOUT = 10

def buscar_lugares(api_key, lat, lng, radio, keyword, buscar_telefono):
    """Función sincrónica que envuelve a ``buscar_lugares_async``."""
    return asyncio.run(
        buscar_lugares_async(api_key, lat, lng, radio, keyword, buscar_telefono)
    )


async def buscar_lugares_async(api_key, lat, lng, radio, keyword, buscar_telefono) -> List[dict]:
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radio,
        "keyword": keyword,
        "key": api_key,
    }
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()

        resultados = []
        tareas = []
        tiendas_detalle = []
        for lugar in data.get("results", []):
            tienda = lugar.copy()
            tienda["telefono"] = "No disponible"
            tienda["categoria"] = "No especificada"
            resultados.append(tienda)

            if buscar_telefono and "place_id" in lugar:
                tiendas_detalle.append(tienda)
                tareas.append(
                    obtener_detalles_async(session, api_key, lugar["place_id"])
                )

        if tareas:
            detalles = await asyncio.gather(*tareas, return_exceptions=True)
            for tienda, detalle in zip(tiendas_detalle, detalles):
                if isinstance(detalle, tuple):
                    tel, cat = detalle
                    if tel:
                        tienda["telefono"] = tel
                    if cat:
                        tienda["categoria"] = cat

        return resultados

async def obtener_detalles_async(session, api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,types",
        "key": api_key,
    }
    try:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
    except aiohttp.ClientError:
        return None, None

    telefono = "No disponible"
    categoria = "No especificada"
    if data.get("status") == "OK" and "result" in data:
        result = data["result"]
        if "formatted_phone_number" in result:
            telefono = result["formatted_phone_number"]
        if "types" in result and isinstance(result["types"], list) and result["types"]:
            categoria = result["types"][0].replace("_", " ").title()

    return telefono, categoria
