# Visor de Tiendas

Aplicación para buscar negocios en la API de Google Maps y visualizarlos desde una interfaz web o mediante una API REST.

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Debes proporcionar la clave de Google Maps mediante la variable de entorno `GOOGLE_API_KEY`. Puedes crear un archivo `.env` con el contenido:

```
GOOGLE_API_KEY=tu_clave_aqui
```

La aplicación leerá este archivo automáticamente.

## Uso

### Interfaz Streamlit

```bash
streamlit run app_refactor.py
```

### API REST

```bash
uvicorn api_busqueda:app --reload
```

Luego visita `http://127.0.0.1:8000/docs` para probar los endpoints.

## Pruebas

Ejecuta los tests con:

```bash
pytest
```
