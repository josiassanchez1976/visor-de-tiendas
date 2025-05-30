import json
from rapidfuzz import fuzz
from json import JSONDecodeError

TIENDAS_FILE = "tiendas_guardadas.json"

def cargar_memoria():
    """Carga la memoria desde ``memoria.json`` manejando errores comunes."""
    try:
        with open("memoria.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except JSONDecodeError:
        # Archivo corrupto
        return []

def guardar_memoria(memoria):
    with open("memoria.json", "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

def ya_existe(tienda, memoria, umbral=85):
    """Comprueba si una tienda ya existe comparando dirección y nombre."""
    for t in memoria:
        if t["Dirección"].strip().lower() == tienda["Dirección"].strip().lower():
            return comparar_nombres(t["Nombre"], tienda["Nombre"], umbral)
    return False

def comparar_nombres(n1: str, n2: str, umbral: int = 85) -> bool:
    """Determina si dos nombres se refieren al mismo negocio usando similitud de cadenas."""
    if not n1 or not n2:
        return False
    similitud = fuzz.token_set_ratio(n1.lower(), n2.lower())
    return similitud >= umbral


def _actualizar_tiendas_guardadas(memoria):
    """Escribe ``tiendas_guardadas.json`` a partir de la memoria."""
    datos = {}
    for item in memoria:
        estado = item["Estado"].strip().lower()
        ciudad = item["Ciudad"].strip().lower()
        datos.setdefault(estado, {}).setdefault(ciudad, [])
        nueva = {
            "tienda": item["Nombre"],
            "categoria": item.get("Categoría", "No especificada"),
            "direccion": item["Dirección"],
            "telefono": item["Teléfono"],
        }
        if nueva not in datos[estado][ciudad]:
            datos[estado][ciudad].append(nueva)
    with open(TIENDAS_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def eliminar_tienda(indice: int) -> bool:
    """Elimina una tienda por índice de ``memoria.json``."""
    memoria = cargar_memoria()
    if 0 <= indice < len(memoria):
        memoria.pop(indice)
        guardar_memoria(memoria)
        _actualizar_tiendas_guardadas(memoria)
        return True
    return False


def eliminar_por_categoria(categoria: str) -> int:
    """Elimina todas las tiendas de una categoría y devuelve cuántas fueron borradas."""
    memoria = cargar_memoria()
    nueva_mem = [t for t in memoria if t.get("Categoría", "") != categoria]
    eliminadas = len(memoria) - len(nueva_mem)
    if eliminadas:
        guardar_memoria(nueva_mem)
        _actualizar_tiendas_guardadas(nueva_mem)
    return eliminadas
