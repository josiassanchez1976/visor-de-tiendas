
import json
import os
from memoria import cargar_memoria, guardar_memoria, ya_existe
from geocoding import obtener_coordenadas_y_radio
from places_search import buscar_lugares

TIENDAS_FILE = "tiendas_guardadas.json"
API_KEY = "AIzaSyBOcCSXuwaRlQ3s0ttDcMOLBswCMjzsRYg"  

def guardar_tiendas_formateadas(memoria):
    datos = {}
    for item in memoria:
        estado = item["Estado"].strip().lower()
        ciudad = item["Ciudad"].strip().lower()
        datos.setdefault(estado, {}).setdefault(ciudad, [])
        nueva = {
            "tienda": item["Nombre"],
            "categoria": item.get("Categoría", "No especificada"),
            "direccion": item["Dirección"],
            "telefono": item["Teléfono"]
        }
        if nueva not in datos[estado][ciudad]:
            datos[estado][ciudad].append(nueva)
    with open(TIENDAS_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def ejecutar_busqueda(estado, ciudades, keywords, optimizar, buscar_telefono):
    memoria = cargar_memoria()
    total_nuevas = 0
    errores = []

    if not os.path.exists("output"):
        os.makedirs("output")

    for ciudad in ciudades:
        lat, lng, radio = obtener_coordenadas_y_radio(API_KEY, ciudad)
        if not lat or not lng:
            errores.append(f"{ciudad}, {estado} - NO se encontraron coordenadas.")
            continue

        for kw in keywords[:]:
            resultados = buscar_lugares(API_KEY, lat, lng, radio, kw, buscar_telefono)
            nuevos = 0
            for lugar in resultados:
                tienda = {
                    "Nombre": lugar.get("name", "N/A"),
                    "Dirección": lugar.get("vicinity", "N/A"),
                    "Ciudad": ciudad,
                    "Estado": estado,
                    "Teléfono": lugar.get("telefono", "No disponible"),
                    "Categoría": lugar.get("categoria", "No especificada")
                }
                if not ya_existe(tienda, memoria):
                    memoria.append(tienda)
                    nuevos += 1
            total_nuevas += nuevos

            if optimizar and nuevos == 0:
                keywords.remove(kw)

    guardar_memoria(memoria)
    guardar_tiendas_formateadas(memoria)

    if errores:
        with open("errores.txt", "a", encoding="utf-8") as f:
            for e in errores:
                f.write(e + "\n")

    print(f"✅ Total nuevas tiendas: {total_nuevas}")
