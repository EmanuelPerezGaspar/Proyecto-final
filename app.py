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
    iniciales = {
        "Creality PLA - Negro": 399,
        "Creality PLA - Blanco": 399,
        "Mexico Maker PETG - Negro": 380,
    }
    guardar_materiales(iniciales)
    return iniciales

def guardar_materiales(diccionario):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)

if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_materiales()

# ==================== CONFIGURACIÓN (SIDEBAR) ====================
st.sidebar.header("⚙️ Parametros básicos")

impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"], key="impresora_select")

if impresora == "A1 MINI":
    consumo = 280
    costo_maquina_hora = 14999 / 6000
else:
    consumo = 350
    costo_maquina_hora = 25000 / 6000

st.sidebar.metric("Costo por hora de máquina (desgaste)", f"${costo_maquina_hora:.2f}")

margen_ganancia = st.sidebar.number_input("Margen de ganancia deseado (%)", value=65.0, step=5.0, min_value=0.0, max_value=500.0, key="margen_input") / 100

aplicar_mano_obra = st.sidebar.checkbox("¿Aplicar costo de mano de obra?", value=True, key="mano_obra_check")
if aplicar_mano_obra:
    costo_mano_obra_hora = st.sidebar.number_input("Costo mano de obra por hora ($)", value=20.0, step=5.0, min_value=0.0, key="costo_hora_mano")
    horas_mano_obra = st.sidebar.number_input("Horas de mano de obra", value=2.0, step=0.5, min_value=0.0, key="horas_mano")
else:
    costo_mano_obra_hora = 0.0
    horas_mano_obra = 0.0

aplicar_iva = st.sidebar.checkbox("¿Aplicar IVA (16%)?", value=True, key="iva_check")

st.sidebar.metric("💡 Costo electricidad kWh", "5.00 MXN")
costo_electricidad = 5.00

st.sidebar.metric("🛠️ Margen de falla", "10 %")
margen_falla = 0.10

# ==================== GESTOR DE MATERIALES ====================
with st.sidebar.expander("➕ Agregar Nuevo Material"):
    nuevo_nombre = st.text_input("Nombre completo del material", key="nuevo_nombre")
    nuevo_precio = st.number_input("Precio por kg ($)", min_value=0.0, value=399.0, step=10.0, key="nuevo_precio")
    if st.button("Agregar Material", key="btn_agregar"):
        if nuevo_nombre.strip():
            st.session_state.materiales[nuevo_nombre.strip()] = nuevo_precio
            guardar_materiales(st.session_state.materiales)
            st.success(f"✅ {nuevo_nombre} agregado")
        else:
            st.error("Escribe un nombre")

with st.sidebar.expander("🗑️ Eliminar Material"):
    if st.session_state.materiales:
        material_a_eliminar = st.selectbox("Selecciona material a eliminar", options=list(st.session_state.materiales.keys()), key="eliminar_select")
        if st.button("Eliminar Material", type="secondary", key="btn_eliminar"):
            if material_a_eliminar in st.session_state.materiales:
                del st.session_state.materiales[material_a_eliminar]
                guardar_materiales(st.session_state.materiales)
                st.success(f"🗑️ {material_a_eliminar} eliminado")

# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", key="cliente_input")

es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False, key="multicolor_check")
multiples_impresiones = st.checkbox("¿La impresión consta de más de una impresión?", value=False, key="multiples_check")

materiales_lista = list(st.session_state.materiales.keys())

# Materiales y Tiempo (mantengo la lógica anterior)
if es_multicolor:
    st.subheader("Materiales (hasta 6)")
    num_materiales = st.slider("Cantidad de materiales diferentes", min_value=2, max_value=6, value=3, key="num_mat_slider")
    peso_total = 0.0
    for i in range(num_materiales):
        col1, col2 = st.columns([3, 1])
        with col1:
            mat = st.selectbox(f"Material {i+1}", materiales_lista, key=f"mat_{i}")
        with col2:
            peso = st.number_input(f"Gramos {i+1}", min_value=0.0, value=None, step=1.0, key=f"peso_{i}", placeholder="0.0")
        peso_total += peso if peso is not None else 0
else:
    col_mat, col_peso = st.columns([3, 2])
    with col_mat:
        material = st.selectbox("Material principal", materiales_lista, key="material_principal")
    with col_peso:
        peso_total = st.number_input("Peso TOTAL filamento (gramos)", min_value=0.0, value=None, step=1.0, placeholder="0.0", key="peso_total")

# (El resto del código de tiempo y cálculo se mantiene igual - para no hacer el mensaje demasiado largo)

if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True, key="calcular_btn"):
    # ... (cálculo completo - si quieres te lo mando en el siguiente mensaje)
    st.info("Cálculo en proceso... (versión completa en el siguiente paso)")

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
