# Visor de Tiendas

Este proyecto permite buscar negocios como ferreterías o proveedores de materiales en ciudades de Estados Unidos utilizando la API de Google Maps. Los resultados se almacenan en archivos JSON y pueden revisarse desde una interfaz en Streamlit o mediante una API construida con FastAPI.

## Configuración rápida

1. Instala las dependencias principales:
   ```bash
   pip install -r requirements.txt
   ```
2. (Opcional) Instala `ollama` si deseas que `memoria.py` compare nombres de tiendas mediante LLM.
3. Proporciona tu clave de Google Maps exportando la variable de entorno `GOOGLE_API_KEY` o editando `runner.py`:
   ```bash
   export GOOGLE_API_KEY=<tu_clave>
   ```

## Ejecutar la aplicación Streamlit

```bash
streamlit run app_refactor.py
```

## Ejecutar la API REST

```bash
uvicorn api_busqueda:app --reload
```

La documentación interactiva está disponible en `http://127.0.0.1:8000/docs`.

## Ejemplo de uso de la API

Realiza una petición POST a `/buscar` con el siguiente formato:

```json
{
  "estado": "texas",
  "ciudades": ["austin", "houston"],
  "keywords": ["hardware store"],
  "optimizar": false,
  "buscar_telefono": true
}
```

## Notas adicionales

- `runner.py` lee de `memoria.json` y actualiza `tiendas_guardadas.json` con los negocios encontrados.
- `memoria.py` utiliza el comando `ollama` de forma opcional para comparar nombres y evitar duplicados.
- Puedes ejecutar pruebas con `pytest test_app.py` si se dispone de archivos de prueba.
