import streamlit as st
import json
import os
import pandas as pd

# ==================== CONFIGURACIÓN VISUAL ====================
st.set_page_config(page_title="Mini Prints", layout="centered", page_icon="🖨️")

st.markdown("""
<style>
    .main { background-color: #0a0a0f; color: #e2e4f0; }
    h1 { color: #f97316; font-size: 3rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.2rem; }
    h2, h3 { color: #f1f5f9; }
    .stMetric { 
        background: #161820; 
        border: 1px solid #334155; 
        border-radius: 16px; 
        padding: 18px 20px;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #f97316, #fb923c); 
        color: white; 
        border-radius: 12px; 
        height: 58px; 
        font-size: 18px; 
        font-weight: 700;
    }
    .dataframe { background: #161820; border: 1px solid #334155; border-radius: 12px; }
    .stExpander { border: 1px solid #334155; border-radius: 12px; background: #161820; }
    label { color: #94a3b8; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.title("🖨️ Mini Prints")
st.markdown("**Cotizador Profesional 3D**")

# ==================== RESTO DE TU CÓDIGO (sin cambios) ====================
# ==================== GESTOR DE MATERIALES ====================
DATA_FILE = "materiales.json"

def cargar_materiales():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        iniciales = {
            "Creality PLA - Negro": 399,
            "Mexico Maker PLA PRO - Azul Talavera": 399,
            "Mexico Maker PLA MATTE - Negro Carbon": 460,
            "Mexico Maker PLA FLEX - Naranja": 449,
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
impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"])
if impresora == "A1 MINI":
    consumo = 280
    costo_maquina_hora = 14999 / 6000
else:
    consumo = 350
    costo_maquina_hora = 25000 / 6000

st.sidebar.metric("Costo por hora de máquina (desgaste)", f"${costo_maquina_hora:.2f}")

margen_ganancia = st.sidebar.number_input("Margen de ganancia deseado (%)", value=65.0, step=5.0, min_value=0.0, max_value=500.0) / 100

aplicar_mano_obra = st.sidebar.checkbox("¿Aplicar costo de mano de obra?", value=True)
if aplicar_mano_obra:
    costo_mano_obra_hora = st.sidebar.number_input("Costo mano de obra por hora ($)", value=20.0, step=5.0, min_value=0.0)
    horas_mano_obra = st.sidebar.number_input("Horas de mano de obra", value=2.0, step=0.5, min_value=0.0)
else:
    costo_mano_obra_hora = 0.0
    horas_mano_obra = 0.0

aplicar_iva = st.sidebar.checkbox("¿Aplicar IVA (16%)?", value=True)
if aplicar_iva:
    st.sidebar.metric("📌 IVA aplicado", "16 %")
    iva = 0.16
else:
    iva = 0.0

st.sidebar.metric("💡 Costo electricidad kWh", "5.00 MXN")
costo_electricidad = 5.00

st.sidebar.metric("🛠️ Margen de falla", "10 %")
margen_falla = 0.10

# Gestor de Materiales (mantengo igual)
with st.sidebar.expander("➕ Agregar Nuevo Material"):
    nuevo_nombre = st.text_input("Nombre completo del material")
    nuevo_precio = st.number_input("Precio por kg ($)", min_value=0.0, value=350.0, step=10.0)
    if st.button("Agregar Material"):
        if nuevo_nombre.strip():
            st.session_state.materiales[nuevo_nombre.strip()] = nuevo_precio
            guardar_materiales(st.session_state.materiales)
            st.success(f"✅ {nuevo_nombre} agregado")
        else:
            st.error("Escribe un nombre")

with st.sidebar.expander("🗑️ Eliminar Material"):
    if st.session_state.materiales:
        material_a_eliminar = st.selectbox("Selecciona material a eliminar", options=list(st.session_state.materiales.keys()))
        if st.button("Eliminar Material", type="secondary"):
            if material_a_eliminar in st.session_state.materiales:
                del st.session_state.materiales[material_a_eliminar]
                guardar_materiales(st.session_state.materiales)
                st.success(f"🗑️ {material_a_eliminar} eliminado")

# ==================== EL RESTO DE TU CÓDIGO (Datos, Materiales, Tiempo, Cálculo) ====================
# (Pega aquí el resto de tu código anterior desde "# ==================== DATOS DE LA IMPRESIÓN ====================" hasta el final)

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
