
import streamlit as st
import json
import os
from runner import ejecutar_busqueda

st.set_page_config(page_title="Buscador Inteligente de Tiendas", layout="wide")
st.title("🔍 Buscador Inteligente de Tiendas")

KEYWORDS = [
    "rebar supply", "steel supply", "building materials", "hardware store",
    "suministro de acero", "varilla", "ferretería", "tienda de materiales", "concrete reinforcement"
]
ARCHIVO_TIENDAS = "tiendas_guardadas.json"
ARCHIVO_NOTAS = "notas_guardadas.json"
ARCHIVO_CIUDADES = "ciudades_estados_completo.json"

def cargar_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def mostrar_tienda(tienda, index, notas_guardadas):
    st.markdown(f"#### 🏬 {tienda['Nombre']}")
    st.markdown(f"📍 Dirección: {tienda['Dirección']}")
    st.markdown(f"📞 Teléfono: {tienda['Teléfono']}")
    st.markdown(f"🏷️ Categoría: {tienda['Categoría']}")
    st.markdown(f"🌆 Ciudad: {tienda['Ciudad']} | 🌎 Estado: {tienda['Estado']}")
    url = f"https://www.google.com/maps/search/?api=1&query={tienda['Nombre'].replace(' ', '+')}+{tienda['Dirección'].replace(' ', '+')}"
    st.markdown(f"[🌍 Ver en Google Maps]({url})", unsafe_allow_html=True)
    texto_completo = f"{tienda['Nombre']} - {tienda['Dirección']} - {tienda['Ciudad']} - {tienda['Estado']} - {tienda['Teléfono']} - {tienda['Categoría']}"
    st.code(texto_completo)

    key_nota = f"{tienda['Estado']}_{tienda['Ciudad']}_{tienda['Nombre']}"
    nota_actual = notas_guardadas.get(key_nota, "")
    nueva_nota = st.text_area(f"📝 Nota para {tienda['Nombre']}", value=nota_actual, key=f"nota_{index}")
    if st.button(f"💾 Guardar nota {index}"):
        notas_guardadas[key_nota] = nueva_nota
        guardar_json(ARCHIVO_NOTAS, notas_guardadas)
        st.success("📝 Nota guardada")
    st.markdown("---")

# BÚSQUEDA MANUAL
st.header("📌 Búsqueda Manual por Estado y Ciudad")
estado = st.text_input("Estado (ej: texas)").strip().lower()
ciudades_input = st.text_area("Lista de ciudades separadas por coma (opcional)").strip()
selected_keywords = st.multiselect("Palabras clave", KEYWORDS, default=KEYWORDS)
palabras_adicionales = st.text_input("Palabras clave adicionales (separadas por comas)").strip()
extra_keywords = [kw.strip() for kw in palabras_adicionales.split(',') if kw.strip()]
todas_keywords = selected_keywords + extra_keywords
buscar_telefono = st.checkbox("¿Buscar teléfonos?", value=True)

if st.button("🔎 Buscar por ciudades"):
    if not estado:
        st.warning("Debes ingresar un estado.")
    else:
        ciudades = [c.strip().lower() for c in ciudades_input.split(",") if c.strip()]
        ejecutar_busqueda(estado, ciudades, todas_keywords, optimizar=False, buscar_telefono=buscar_telefono)
        st.success("✅ Búsqueda manual completada.")

# BÚSQUEDA GLOBAL POR ESTADO
st.header("🌎 Búsqueda Global por Estado")
estados_ciudades = cargar_json(ARCHIVO_CIUDADES)

if estados_ciudades:
    estado_global = st.selectbox("Selecciona un estado", sorted(estados_ciudades.keys()))
    keywords_global = st.multiselect("Palabras clave (global)", KEYWORDS, default=KEYWORDS)
    palabras_adicionales_global = st.text_input("Palabras clave adicionales (global, separadas por comas)").strip()
    extra_keywords_global = [kw.strip() for kw in palabras_adicionales_global.split(',') if kw.strip()]
    todas_keywords_global = keywords_global + extra_keywords_global
    buscar_tel_global = st.checkbox("¿Buscar teléfonos? (global)", value=True)

    if st.button("🔍 Buscar en todas las ciudades del estado"):
        ciudades = estados_ciudades.get(estado_global, [])
        ejecutar_busqueda(estado_global, ciudades, todas_keywords_global, optimizar=False, buscar_telefono=buscar_tel_global)
        st.success(f"✅ Búsqueda completada en {len(ciudades)} ciudades de {estado_global.upper()}.")

# VISOR DE TIENDAS GUARDADAS
st.header("📋 Visor de Tiendas Guardadas")
tiendas = cargar_json(ARCHIVO_TIENDAS)
notas_guardadas = cargar_json(ARCHIVO_NOTAS)

datos = []
for estado_k, ciudades_k in tiendas.items():
    for ciudad_k, lista in ciudades_k.items():
        for tienda in lista:
            datos.append({
                "Estado": estado_k,
                "Ciudad": ciudad_k,
                "Nombre": tienda.get("tienda", "Sin nombre"),
                "Dirección": tienda.get("direccion", "Desconocida"),
                "Teléfono": tienda.get("telefono", "No disponible"),
                "Categoría": tienda.get("categoria", "No especificada")
            })

if not datos:
    st.warning("❗️ No hay tiendas guardadas aún.")
else:
    estado_sel = st.selectbox("Filtrar por estado", ["Todos"] + sorted({d["Estado"] for d in datos}))
    ciudad_sel = st.selectbox("Filtrar por ciudad", ["Todos"] + sorted({d["Ciudad"] for d in datos if d["Estado"] == estado_sel or estado_sel == "Todos"}))
    filtrados = [d for d in datos if (estado_sel == "Todos" or d["Estado"] == estado_sel) and (ciudad_sel == "Todos" or d["Ciudad"] == ciudad_sel)]

    st.markdown(f"### 🏪 Total tiendas: {len(filtrados)}")
    for i, tienda in enumerate(filtrados):
        mostrar_tienda(tienda, i, notas_guardadas)
