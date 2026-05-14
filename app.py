import streamlit as st

st.set_page_config(page_title="Calculadora de Precios", layout="centered")

st.title("🖨️ Mini Prints")

# ==================== CONFIGURACIÓN (SIDEBAR) ====================
st.sidebar.header("⚙️ Parametros básicos")

# Margen de Ganancia (editable y permite más del 100%)
margen_ganancia = st.sidebar.number_input(
    "Margen de ganancia deseado (%)", 
    value=65.0, 
    step=5.0, 
    min_value=0.0, 
    max_value=500.0
) / 100

# Selección de impresora
impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"])

if impresora == "A1 MINI":
    consumo = 280
    costo_maquina_hora = 12
else:
    consumo = 350
    costo_maquina_hora = 18

# Valores FIJOS
st.sidebar.metric("💡 Costo electricidad kWh", "5.00 MXN")
costo_electricidad = 5.00

st.sidebar.metric("🛠️ Margen de falla", "10 %")
margen_falla = 0.10

# Mano de Obra Opcional
aplicar_mano_obra = st.sidebar.checkbox("¿Aplicar costo de mano de obra?", value=True)

if aplicar_mano_obra:
    costo_mano_obra_hora = st.sidebar.number_input("Costo mano de obra por hora ($)", value=20.0, step=5.0, min_value=0.0)
    horas_mano_obra = st.sidebar.number_input("Horas de mano de obra", value=2.0, step=0.5, min_value=0.0)
else:
    costo_mano_obra_hora = 0.0
    horas_mano_obra = 0.0

# IVA con checkbox (solo se muestra cuando está activado)
aplicar_iva = st.sidebar.checkbox("¿Aplicar IVA (16%)?", value=True)

if aplicar_iva:
    st.sidebar.metric("📌 IVA aplicado", "16 %")
    iva = 0.16
else:
    iva = 0.0


# ==================== DATOS DE LA IMPRESIÓN ====================
st.header("📋 Datos de la impresión")

cliente = st.text_input("Cliente / Modelo", "Emanuel")

# Multicolor
es_multicolor = st.checkbox("¿Es impresión multicolor?", value=False)

# ==================== MATERIALES DINÁMICOS ====================
materiales_usados = []
pesos_usados = []

if es_multicolor:
    st.subheader("Materiales (hasta 6)")
    num_materiales = st.slider("Cantidad de materiales diferentes", min_value=1, max_value=6, value=3)
    
    for i in range(num_materiales):
        col1, col2 = st.columns([3, 1])
        with col1:
            mat = st.selectbox(f"Material {i+1}", [
                "Creality PLA - Negro",
                "Mexico Maker PLA PRO - Azul Talavera",
                "Mexico Maker PLA MATTE - Negro Carbon",
                "Mexico Maker PLA FLEX - Naranja",
                "Mexico Maker PETG - Negro",
                "Otro"
            ], key=f"mat_{i}")
        with col2:
            peso = st.number_input(f"Gramos {i+1}", min_value=0.0, value=20.0, step=1.0, key=f"peso_{i}")
        
        materiales_usados.append(mat)
        pesos_usados.append(peso)
else:
    # Un solo material
    material = st.selectbox("Material principal", [
        "Creality PLA - Negro",
        "Mexico Maker PLA PRO - Azul Talavera",
        "Mexico Maker PLA MATTE - Negro Carbon",
        "Mexico Maker PLA FLEX - Naranja",
        "Mexico Maker PETG - Negro"
    ])
    peso_total = st.number_input("Peso TOTAL filamento (gramos)", min_value=1.0, value=6.0, step=1.0)

# ==================== RESTO DE CAMPOS ====================
col1, col2 = st.columns(2)
with col1:
    tiempo_impresion = st.number_input("Tiempo total de impresión (horas)", min_value=0.1, value=14.0, step=0.1)
    num_placas = st.number_input("Número de placas", min_value=1, value=2)

# ==================== CÁLCULO ====================
if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True):
    
    if es_multicolor:
        # Sumar pesos y calcular costo promedio (simple)
        peso_total = sum(pesos_usados)
        # Por simplicidad usamos precio promedio (puedes mejorarlo después)
        precio_kg = 430  # Promedio aproximado
    else:
        precio_kg = 399 if "Creality" in material else 460
    
    costo_material = (peso_total / 1000) * precio_kg
    costo_electricidad_total = tiempo_impresion * (consumo / 1000) * costo_electricidad
    costo_maquina_total = tiempo_impresion * costo_maquina_hora
    costo_mano_obra_total = horas_mano_obra * costo_mano_obra_hora
   
    subtotal = costo_material + costo_electricidad_total + costo_maquina_total + costo_mano_obra_total
    subtotal_con_falla = subtotal * (1 + margen_falla)
   
    precio_final = subtotal_con_falla / (1 - margen_ganancia) * (1 + iva)
   
    st.success(f"**PRECIO FINAL: ${precio_final:,.2f} MXN**")
   
    st.divider()
    st.write("### 📊 Desglose detallado:")
    st.write(f"**Material:** ${costo_material:,.2f} ({peso_total}g)")
    st.write(f"**Electricidad:** ${costo_electricidad_total:,.2f}")
    st.write(f"**Máquina:** ${costo_maquina_total:,.2f}")
    if aplicar_mano_obra:
        st.write(f"**Mano de obra:** ${costo_mano_obra_total:,.2f} ({horas_mano_obra} horas)")
    st.write(f"**Subtotal + Falla:** ${subtotal_con_falla:,.2f}")
    
    if aplicar_iva:
        st.write(f"**IVA (16%):** ${precio_final - (subtotal_con_falla / (1 - margen_ganancia)) :,.2f}")

st.caption("Calculadora 3D © 2026")
st.caption("Powered by Mini Prints")
