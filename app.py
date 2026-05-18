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

# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", "")

es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False)
multiples_impresiones = st.checkbox("¿La impresión consta de más de una impresión?", value=False)

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
if multiples_impresiones:
    st.subheader("Tiempos por impresión")
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

# ==================== NÚMERO DE PIEZAS ====================
num_piezas = st.number_input("Número de piezas / figuras que se obtienen", 
                             min_value=1, 
                             value=1, 
                             step=1, 
                             placeholder="1")

# ==================== CÁLCULO ====================
if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True):
    
    if es_multicolor:
        costo_material_total = 0.0
        detalles_materiales = []
        for i in range(num_materiales):
            mat_key = f"mat_{i}"
            peso_key = f"peso_{i}"
            material_actual = st.session_state.get(mat_key, "Desconocido")
            peso_actual = st.session_state.get(peso_key, 0)
            precio_actual = st.session_state.materiales.get(material_actual, 400)
            costo_individual = (peso_actual / 1000) * precio_actual
            costo_material_total += costo_individual
            detalles_materiales.append({
                "Material": material_actual,
                "Gramaje (g)": peso_actual,
                "Precio/kg ($)": precio_actual,
                "Costo ($)": round(costo_individual, 2)
            })
    else:
        costo_material_total = (peso_total / 1000) * precio_kg
        detalles_materiales = [{
            "Material": material,
            "Gramaje (g)": peso_total,
            "Precio/kg ($)": precio_kg,
            "Costo ($)": round(costo_material_total, 2)
        }]

    costo_electricidad_total = tiempo_total * (consumo / 1000) * costo_electricidad
    costo_maquina_total = tiempo_total * costo_maquina_hora
    costo_mano_obra_total = horas_mano_obra * costo_mano_obra_hora if aplicar_mano_obra else 0
   
    # === COSTO DE PRODUCCIÓN ===
    costo_produccion = costo_material_total + costo_electricidad_total + costo_maquina_total + costo_mano_obra_total
    costo_con_falla = costo_produccion * (1 + margen_falla)
    
    # === GANANCIA ===
    precio_sin_iva = costo_con_falla / (1 - margen_ganancia)
    ganancia = precio_sin_iva - costo_con_falla
    
    # === IVA ===
    iva_monto = precio_sin_iva * iva if aplicar_iva else 0
    precio_final = precio_sin_iva + iva_monto

    st.success(f"**PRECIO FINAL: ${precio_final:,.2f} MXN**")
   
    st.divider()
    
    # ==================== RESUMEN FINAL ====================
    st.write("### 📊 Resumen Final")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("**Costo de Producción**", f"${costo_produccion:,.2f}")
        st.metric("**Ganancia**", f"${ganancia:,.2f} ({margen_ganancia*100:.0f}%)")
    with col2:
        st.metric("**Subtotal + Falla**", f"${costo_con_falla:,.2f}")
        st.metric("**IVA**", f"${iva_monto:,.2f}" if aplicar_iva else "$0.00")
    
    st.write("**────────────────────**")
    st.success(f"**TOTAL A COBRAR: ${precio_final:,.2f} MXN**")

    # ==================== DESGLOSE DETALLADO ====================
    st.divider()
    st.write("### 📋 Desglose Detallado")
    
    st.write("**🧵 Materiales utilizados:**")
    st.dataframe(pd.DataFrame(detalles_materiales), use_container_width=True, hide_index=True)
    
    st.write("**⚡ Costo de Electricidad:**")
    data_elec = {
        "Concepto": ["Consumo impresora", "Tiempo total", "Energía consumida", "Costo por kWh", "Costo total"],
        "Valor": [f"{consumo} Watts", f"{tiempo_total:.2f} h", f"{tiempo_total*(consumo/1000):.3f} kWh", f"${costo_electricidad}/kWh", f"${costo_electricidad_total:,.2f}"]
    }
    st.dataframe(pd.DataFrame(data_elec), use_container_width=True, hide_index=True)
    
    st.write("**🔧 Costo de Máquina:**")
    data_maquina = {
        "Concepto": ["Costo por hora", "Tiempo total", "Costo total máquina"],
        "Valor": [f"${costo_maquina_hora:.2f}", f"{tiempo_total:.2f} horas", f"${costo_maquina_total:,.2f}"]
    }
    st.dataframe(pd.DataFrame(data_maquina), use_container_width=True, hide_index=True)

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
