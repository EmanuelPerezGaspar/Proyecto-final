import streamlit as st
import json
import os

st.set_page_config(page_title="Calculadora de Precios", layout="centered")
st.title("🖨️ Mini Prints")

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
    costo_maquina_hora = 12
else:
    consumo = 350
    costo_maquina_hora = 18

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

# Gestor de Materiales
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
    else:
        st.write("No hay materiales")

# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", "")

es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False)

materiales_lista = list(st.session_state.materiales.keys())

# ==================== MATERIALES ====================
if es_multicolor:
    st.subheader("Materiales (hasta 6)")
    num_materiales = st.slider("Cantidad de materiales diferentes", min_value=2, max_value=6, value=3)
    peso_total = 0.0
    for i in range(num_materiales):
        col1, col2 = st.columns([3, 1])
        with col1:
            mat = st.selectbox(f"Material {i+1}", materiales_lista, key=f"mat_{i}")
        with col2:
            peso = st.number_input(f"Gramos {i+1}", min_value=0.0, value=None, step=1.0, key=f"peso_{i}", placeholder="0.0")
        peso_total += peso if peso is not None else 0
    precio_kg = 430
else:
    col_mat, col_peso = st.columns([3, 2])
    with col_mat:
        material = st.selectbox("Material principal", materiales_lista)
    with col_peso:
        peso_total = st.number_input("Peso TOTAL filamento (gramos)", min_value=0.0, value=None, step=1.0, placeholder="0.0")
    precio_kg = st.session_state.materiales.get(material, 400)

# ==================== TIEMPO DE IMPRESIÓN ====================
 st.subheader("Tiempos por impresión")
multiples_impresiones = st.checkbox("¿La impresión consta de más de una impresión?", value=False)

if multiples_impresiones:
   
    num_impresiones = st.slider("Cantidad de impresiones", min_value=2, max_value=10, value=2)
    tiempo_total = 0.0
    for i in range(num_impresiones):
        col1, col2 = st.columns([2, 1])
        with col1:
            horas = st.number_input(f"Horas impresión {i+1}", min_value=0, value=None, step=1, key=f"horas_{i}", placeholder="0")
        with col2:
            minutos = st.number_input(f"Minutos impresión {i+1}", min_value=0, max_value=59, value=None, step=1, key=f"min_{i}", placeholder="0")
        tiempo_total += (horas or 0) + ((minutos or 0) / 60)
else:
    st.subheader("Tiempo de impresión")
    col1, col2 = st.columns([2, 1])
    with col1:
        horas = st.number_input("Horas", min_value=0, value=None, step=1, placeholder="0")
    with col2:
        minutos = st.number_input("Minutos", min_value=0, max_value=59, value=None, step=1, placeholder="0")
    tiempo_total = (horas or 0) + ((minutos or 0) / 60)

num_placas = st.number_input("Número de placas", min_value=1, value=None, step=1, placeholder="1")

# ==================== CÁLCULO ====================
if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True):
    
    costo_material = (peso_total / 1000) * precio_kg
    costo_electricidad_total = tiempo_total * (consumo / 1000) * costo_electricidad
    costo_maquina_total = tiempo_total * costo_maquina_hora
    costo_mano_obra_total = horas_mano_obra * costo_mano_obra_hora
   
    subtotal = costo_material + costo_electricidad_total + costo_maquina_total + costo_mano_obra_total
    subtotal_con_falla = subtotal * (1 + margen_falla)
    precio_final = subtotal_con_falla / (1 - margen_ganancia) * (1 + iva)
   
    st.success(f"**PRECIO FINAL: ${precio_final:,.2f} MXN**")
   
    st.divider()
    st.write("### 📊 Desglose detallado:")
    st.write(f"**Material:** ${costo_material:,.2f} ({peso_total}g)")
    st.write(f"**Tiempo total:** {tiempo_total:.2f} horas")
    st.write(f"**Electricidad:** ${costo_electricidad_total:,.2f}")
    st.write(f"**Máquina:** ${costo_maquina_total:,.2f}")
    if aplicar_mano_obra:
        st.write(f"**Mano de obra:** ${costo_mano_obra_total:,.2f} ({horas_mano_obra} horas)")
    st.write(f"**Subtotal + Falla:** ${subtotal_con_falla:,.2f}")
    if aplicar_iva:
        st.write(f"**IVA (16%):** ${precio_final - (subtotal_con_falla / (1 - margen_ganancia)) :,.2f}")

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
