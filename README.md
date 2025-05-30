# Visor de Tiendas

Aplicación para buscar negocios en la API de Google Maps y visualizarlos desde una interfaz web o mediante una API REST.

## Instalación

Ejecuta el script `setup.sh` para instalar todas las dependencias:

```bash
./setup.sh
```

## Configuración

Debes proporcionar la clave de Google Maps mediante la variable de entorno `GOOGLE_API_KEY`. Puedes crear un archivo `.env` con el contenido:

```
GOOGLE_API_KEY=tu_clave_aqui
```

La aplicación leerá este archivo automáticamente. Todos los scripts, incluido
`buscador_tiendas_con_categoria.py`, utilizan esta misma variable.

## Uso

### Interfaz Streamlit

```bash
streamlit run app_refactor.py
```

Desde la interfaz podrás guardar notas y ahora también eliminar tiendas
individualmente o por categoría.

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
