import streamlit as st

st.set_page_config(page_title="Calculadora 3D", layout="centered")

st.title("Calculadora de precios")

# Configuración
st.sidebar.header("⚙️ Configuración tecnica")

costo_electricidad = st.sidebar.number_input("Costo electricidad kWh", value=5.0, step=0.1)
costo_mano_obra = st.sidebar.number_input("Costo mano de obra / hora", value=20.0, step=5.0)
margen_falla = st.sidebar.number_input("Margen de falla (%)", value=10, step=1) / 100
margen_ganancia = st.sidebar.number_input("Margen de ganancia (%)", value=65, step=5) / 100
iva = st.sidebar.number_input("IVA (%)", value=16, step=1) / 100

impresora = st.sidebar.selectbox("Impresora", ["A1 MINI", "A1"])

if impresora == "A1 MINI":
    consumo = 280
    costo_maquina = 12
else:
    consumo = 350
    costo_maquina = 18

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
