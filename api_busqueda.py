
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from runner import ejecutar_busqueda

app = FastAPI(title="API Buscador de Tiendas")

class BusquedaRequest(BaseModel):
    estado: str
    ciudades: List[str]
    keywords: List[str]
    optimizar: bool = False
    buscar_telefono: bool = True

@app.get("/")
def root():
    return {"mensaje": "API de Buscador Inteligente de Tiendas"}

@app.post("/buscar")
def buscar(request: BusquedaRequest):
    try:
        ejecutar_busqueda(
            estado=request.estado,
            ciudades=request.ciudades,
            keywords=request.keywords,
            optimizar=request.optimizar,
            buscar_telefono=request.buscar_telefono
        )
        return {"resultado": "Búsqueda completada exitosamente"}
    except Exception as e:
        return {"error": str(e)}
