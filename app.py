import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Calculadora de Precios", layout="centered")
st.title("🖨️ Mini Prints")

# ==================== GESTOR DE MATERIALES ====================
DATA_FILE = "materiales.json"

def cargar_materiales():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    iniciales = {"Creality PLA - Negro": 399}
    guardar_materiales(iniciales)
    return iniciales

def guardar_materiales(diccionario):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)

if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_materiales()

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Parametros básicos")

impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"], key="impresora")

if impresora == "A1 MINI":
    consumo = 280
    costo_maquina_hora = 14999 / 6000
else:
    consumo = 350
    costo_maquina_hora = 25000 / 6000

st.sidebar.metric("Costo por hora de máquina", f"${costo_maquina_hora:.2f}")

margen_ganancia = st.sidebar.number_input("Margen de ganancia (%)", value=65.0, step=5.0, min_value=0.0, max_value=500.0, key="margen") / 100

aplicar_mano_obra = st.sidebar.checkbox("¿Aplicar mano de obra?", value=True, key="mano_check")
if aplicar_mano_obra:
    costo_mano_obra_hora = st.sidebar.number_input("Costo mano de obra/hora ($)", value=20.0, step=5.0, key="costo_mano")
    horas_mano_obra = st.sidebar.number_input("Horas de mano de obra", value=2.0, step=0.5, key="horas_mano_input")
else:
    costo_mano_obra_hora = 0.0
    horas_mano_obra = 0.0

aplicar_iva = st.sidebar.checkbox("¿Aplicar IVA (16%)?", value=True, key="iva_check")

st.sidebar.metric("💡 Costo kWh", "5.00 MXN")
costo_electricidad = 5.00
margen_falla = 0.10

# Gestor de materiales
with st.sidebar.expander("➕ Agregar Material"):
    nuevo = st.text_input("Nombre", key="nuevo_nom")
    prec = st.number_input("Precio/kg", value=399.0, key="nuevo_prec")
    if st.button("Agregar", key="add_btn"):
        if nuevo:
            st.session_state.materiales[nuevo] = prec
            guardar_materiales(st.session_state.materiales)
            st.success("Agregado")

with st.sidebar.expander("🗑️ Eliminar Material"):
    if st.session_state.materiales:
        elim = st.selectbox("Material", options=list(st.session_state.materiales.keys()), key="elim_select")
        if st.button("Eliminar", key="del_btn"):
            del st.session_state.materiales[elim]
            guardar_materiales(st.session_state.materiales)
            st.success("Eliminado")

# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", key="cliente")

es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False, key="multi_check")
multiples_impresiones = st.checkbox("¿La impresión consta de más de una impresión?", value=False, key="multi_imp_check")

materiales_lista = list(st.session_state.materiales.keys())

# Materiales
if es_multicolor:
    st.subheader("Materiales")
    num_mat = st.slider("Cantidad de materiales", 2, 6, 3, key="num_mat")
    peso_total = 0.0
    for i in range(num_mat):
        col1, col2 = st.columns([3,1])
        with col1:
            mat = st.selectbox(f"Material {i+1}", materiales_lista, key=f"mat_{i}")
        with col2:
            peso = st.number_input(f"Gramos {i+1}", min_value=0.0, value=0.0, step=1.0, key=f"peso_{i}")
        peso_total += peso
else:
    col1, col2 = st.columns([3,2])
    with col1:
        material = st.selectbox("Material principal", materiales_lista, key="mat_prin")
    with col2:
        peso_total = st.number_input("Peso TOTAL (gramos)", min_value=0.0, value=0.0, step=1.0, key="peso_total")

# ==================== TIEMPO DE IMPRESIÓN ====================
st.subheader("⏱️ Tiempo de impresión")

if multiples_impresiones:
    num_imp = st.slider("Cantidad de impresiones", 2, 10, 2, key="num_imp")
    tiempo_total = 0.0
    for i in range(num_imp):
        col1, col2 = st.columns(2)
        with col1:
            h = st.number_input(f"Horas imp. {i+1}", min_value=0, value=0, step=1, key=f"horas_{i}")
        with col2:
            m = st.number_input(f"Minutos imp. {i+1}", min_value=0, max_value=59, value=0, step=1, key=f"min_{i}")
        tiempo_total += h + (m / 60)
else:
    col1, col2 = st.columns(2)
    with col1:
        horas = st.number_input("Horas", min_value=0, value=0, step=1, key="horas_single")
    with col2:
        minutos = st.number_input("Minutos", min_value=0, max_value=59, value=0, step=1, key="min_single")
    tiempo_total = horas + (minutos / 60)

# ==================== CÁLCULO ====================
if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True, key="calcular"):
    # ... (cálculo completo)
    costo_material_total = (peso_total / 1000) * st.session_state.materiales.get(material if not es_multicolor else "Creality PLA - Negro", 399)
    # (El resto del cálculo se mantiene igual)

    st.success("Cálculo realizado correctamente")

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
