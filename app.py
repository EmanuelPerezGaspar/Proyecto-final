# ==================== CÁLCULO ====================
if st.button("🚀 Calcular Precio Final", type="primary", use_container_width=True):
    
    # Materiales
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

    # Otros costos
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

    # ==================== DESGLOSE DETALLADO (mantienes lo que ya te gusta) ====================
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
