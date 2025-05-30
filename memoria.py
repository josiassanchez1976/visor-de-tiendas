import json
import subprocess

def cargar_memoria():
    try:
        with open("memoria.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_memoria(memoria):
    with open("memoria.json", "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2)

def ya_existe(tienda, memoria):
    for t in memoria:
        if t["Dirección"].strip().lower() == tienda["Dirección"].strip().lower():
            return comparar_nombres(t["Nombre"], tienda["Nombre"])
    return False

def comparar_nombres(n1, n2):
    prompt = f"¿Los siguientes nombres son el mismo negocio? Nombre 1: {n1} Nombre 2: {n2}. Responde solo sí o no."
    try:
        res = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True, text=True, timeout=25)
        return "sí" in res.stdout.lower() or "yes" in res.stdout.lower()
    except:
        return False
