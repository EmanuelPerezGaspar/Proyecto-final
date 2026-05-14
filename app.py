import streamlit as st

st.set_page_config(page_title="Calculadora de Precios", layout="centered")
st.title("🖨️ Mini Prints")

# ==================== CONFIGURACIÓN (SIDEBAR) ====================
st.sidebar.header("⚙️ Parametros básicos")

margen_ganancia = st.sidebar.number_input(
    "Margen de ganancia deseado (%)",
    value=65.0, step=5.0, min_value=0.0, max_value=500.0
) / 100

impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"])
if impresora == "A1 MINI":
    consumo = 280
    costo_maquina_hora = 12
else:
    consumo = 350
    costo_maquina_hora = 18

st.sidebar.metric("💡 Costo electricidad kWh", "5.00 MXN")
costo_electricidad = 5.00

st.sidebar.metric("🛠️ Margen de falla", "10 %")
margen_falla = 0.10

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

# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", "")

es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False)

# ==================== MATERIALES ====================
if es_multicolor:
    st.subheader("Materiales (hasta 6)")
    num_materiales = st.slider("Cantidad de materiales diferentes", min_value=2, max_value=6, value=3)
    peso_total = 0.0
    for i in range(num_materiales):
        col1, col2 = st.columns([3, 1])
        with col1:
            mat = st.selectbox(f"Material {i+1}", [
                "Creality PLA - Negro", "Mexico Maker PLA PRO - Azul Talavera",
                "Mexico Maker PLA MATTE - Negro Carbon", "Mexico Maker PLA FLEX - Naranja",
                "Mexico Maker PETG - Negro"
            ], key=f"mat_{i}")
        with col2:
            peso = st.number_input(f"Gramos {i+1}", min_value=0.0, value=None, step=1.0, key=f"peso_{i}", placeholder="0.0")
        peso_total += peso if peso is not None else 0
    precio_kg = 430
else:
    col_mat, col_peso = st.columns([3, 2])
    with col_mat:
        material = st.selectbox("Material principal", [
            "Creality PLA - Negro", "Mexico Maker PLA PRO - Azul Talavera",
            "Mexico Maker PLA MATTE - Negro Carbon", "Mexico Maker PLA FLEX - Naranja",
            "Mexico Maker PETG - Negro"
        ])
    with col_peso:
        peso_total = st.number_input("Peso TOTAL filamento (gramos)", min_value=0.0, value=None, step=1.0, placeholder="0.0")
    precio_kg = 399 if "Creality" in material else 460

# ==================== TIEMPO DE IMPRESIÓN ====================

# Nueva pregunta: Múltiples impresiones
multiples_impresiones = st.checkbox("¿La impresión consta de más de una impresión?", value=False)

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
    tiempo_impresion = st.number_input("Tiempo total de impresión (horas)", min_value=0.0, value=None, step=0.1, placeholder="0.0")
    tiempo_total = tiempo_impresion if tiempo_impresion is not None else 0.0

num_placas = st.number_input("Número de placas", min_value=1, value=None, step=1, placeholder="1")
