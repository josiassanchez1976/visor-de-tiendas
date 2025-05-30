# Visor de Tiendas

Aplicación para buscar negocios en la API de Google Maps y visualizarlos desde una interfaz web o mediante una API REST.

## Instalación

Ejecuta el script de preparación para instalar las dependencias:
```bash
./setup.sh
```

## Configuración

Debes proporcionar la clave de Google Maps mediante la variable de entorno `GOOGLE_API_KEY`. Puedes crear un archivo `.env` con el contenido:

```
GOOGLE_API_KEY=tu_clave_aqui
```

La aplicación leerá este archivo automáticamente.
Todas las utilidades de este repositorio (incluido
`buscador_tiendas_con_categoria.py`) utilizan la misma variable
`GOOGLE_API_KEY`.

## Uso

### Interfaz Streamlit

```bash
streamlit run app_refactor.py
```
En el visor puedes eliminar tiendas individuales o borrar todas las de una
categoría mediante los botones disponibles.
La apariencia de la aplicación puede personalizarse editando
``.streamlit/config.toml``.

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
Recuerda ejecutar previamente `./setup.sh` para instalar las dependencias
necesarias.
