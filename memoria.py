import json
from rapidfuzz import fuzz

def cargar_memoria():
    try:
        with open("memoria.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_memoria(memoria):
    with open("memoria.json", "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2)

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
