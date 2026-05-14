import streamlit as st

st.set_page_config(page_title="Calculadora 3D", layout="centered")

st.title("Calculadora de precios")

# ==================== CONFIGURACIÓN ====================
st.sidebar.header("⚙️ Configuración")

# Mano de Obra Opcional
aplicar_mano_obra = st.sidebar.checkbox("¿Aplicar costo de mano de obra?", value=True)

if aplicar_mano_obra:
    costo_mano_obra_hora = st.sidebar.number_input("Costo mano de obra por hora ($)", value=20.0, step=5.0, min_value=0.0)
    horas_mano_obra = st.sidebar.number_input("Horas de mano de obra", value=2.0, step=0.5, min_value=0.0)
else:
    costo_mano_obra_hora = 0.0
    horas_mano_obra = 0.0

# Margen de Ganancia (editable y permite >100%)
margen_ganancia = st.sidebar.number_input(
    "Margen de ganancia deseado (%)", 
    value=65.0, 
    step=5.0, 
    min_value=0.0, 
    max_value=500.0
) / 100

impresora = st.sidebar.selectbox("Impresora usada", ["A1 MINI", "A1"])
if impresora == "A1 MINI":
    consumo = 280
    costo_maquina = 12
else:
    consumo = 350
    costo_maquina = 18

# IVA con checkbox
aplicar_iva = st.sidebar.checkbox("¿Aplicar IVA (16%)?", value=True)
iva = 0.16 if aplicar_iva else 0.0

if aplicar_iva:
    st.sidebar.metric("📌 IVA aplicado", "16 %")
else:
    st.sidebar.metric("📌 IVA aplicado", "0 %")
    
# Valores FIJOS
st.sidebar.metric("💡 Costo electricidad kWh", "5.00 MXN")
costo_electricidad = 5.00

st.sidebar.metric("🛠️ Margen de falla", "10 %")
margen_falla = 0.10

# Datos de la impresión
st.header("📋 Información")

cliente = st.text_input("Cliente / Modelo", "Cliente / Modelo")
tiempo = st.number_input("Tiempo de impresión (horas)", min_value=0.1, value=14.0, step=0.1)
peso = st.number_input("Filamento usado (g)", min_value=1.0, value=6.0, step=1.0)

material = st.selectbox("Filamento", [
    "Creality PLA - Negro",
    "Mexico Maker PLA PRO - Azul Talavera",
    "Mexico Maker PLA MATTE - Negro Carbon"
])

precio_kg = 399 if "Creality" in material else 460

if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True):
    
    costo_mat = (peso / 1000) * precio_kg
    costo_elec = tiempo * (consumo / 1000) * costo_electricidad
    costo_maquina_total = tiempo * costo_maquina
    costo_mano = tiempo * costo_mano_obra
    
    subtotal = costo_mat + costo_elec + costo_maquina_total + costo_mano
    subtotal_falla = subtotal * (1 + margen_falla)
    
    precio_final = subtotal_falla / (1 - margen_ganancia) * (1 + iva)
    
    st.success(f"**PRECIO FINAL: ${precio_final:,.2f} MXN**")
    
    st.write("### Desglose:")
    st.write(f"Material: ${costo_mat:,.2f}")
    st.write(f"Electricidad: ${costo_elec:,.2f}")
    st.write(f"Máquina: ${costo_maquina_total:,.2f}")
    st.write(f"Mano de obra: ${costo_mano:,.2f}")

st.caption("Calculadora personalizada para tus impresiones 3D")
