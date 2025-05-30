import json
import logging
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

def cargar_memoria():
    try:
        with open("memoria.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        logger.error("Error al leer memoria.json: %s", e)
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


def eliminar_tienda(indice: int) -> bool:
    """Elimina una tienda por índice de ``memoria.json``."""
    memoria = cargar_memoria()
    if 0 <= indice < len(memoria):
        del memoria[indice]
        guardar_memoria(memoria)
        return True
    return False


def eliminar_por_categoria(categoria: str) -> int:
    """Elimina todas las tiendas de la categoría dada."""
    memoria = cargar_memoria()
    inicial = len(memoria)
    memoria = [t for t in memoria if t.get("Categoría") != categoria]
    eliminadas = inicial - len(memoria)
    if eliminadas:
        guardar_memoria(memoria)
    return eliminadas
