# visor-de-tiendas

Este proyecto proporciona una API REST para buscar y almacenar tiendas usando la API de Google Maps.
Sigue estos pasos para ejecutarlo de forma local:

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia el servidor FastAPI:
   ```bash
   uvicorn api_busqueda:app --reload
   ```
3. Visita `http://127.0.0.1:8000/docs` para acceder a la documentación interactiva.
