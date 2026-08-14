import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Atelier Virtual | Cotizador de Alta Costura",
    layout="wide",
    page_icon="👗"
)

# --- ESTILOS CSS PERSONALIZADOS (ESTÉICA DE LUJO) ---
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #eaeaea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL ---
st.title("👗 Atelier Virtual: Cotizador de Alta Costura")
st.caption("Sistema profesional de estimación de costos, personalización de prendas a la medida y presupuestos en tiempo real.")
st.markdown("---")

# --- CATALOGOS Y TARIFAS ---
TELAS = {
    "Seda de Mora Orgánica": 65.0,
    "Raso Satinado de Seda": 40.0,
    "Encaje Francés Chantilly": 85.0,
    "Tul Bordado en Hilos de Seda": 55.0,
    "Mikado de Seda Estructurado": 70.0,
    "Gasa / Chiffon de Seda": 35.0,
    "Organza Orgánica Crispy": 38.0,
    "Terciopelo de Seda Premium": 60.0,
    "Algodón Lino Italiano": 28.0
}

SILUETAS = {
    "A-Line / Línea A (Clásica)": 0.0,
    "Sirena / Mermaid (Ajustado)": 60.0,
    "Princesa / Ballgown (Volumen Alto)": 110.0,
    "Corte Recto / Columna Minimalista": 20.0,
    "Evasé Fluido": 30.0,
    "Asimétrico Avant-Garde": 90.0
}

ESCOTES = {
    "Corazón Trapeado": 25.0,
    "Escote en V Profundo": 20.0,
    "Bandeau / Strapless Rígido": 35.0,
    "Cuello Alto / Halter Solemne": 15.0,
    "Hombros Caídos / Off-Shoulder": 40.0,
    "Ilusión en Encaje Transparente": 50.0
}

ESPALDAS = {
    "Espalda Descubierta Profunda": 35.0,
    "Abotonadura de Cristal de la Cera (Manual)": 50.0,
    "Espalda en V Clásica": 15.0,
    "Corsé Ajustable con Lazos": 45.0,
    "Espalda Cerrada Tradicional": 0.0
}

MANGAS = {
    "Sin Mangas / Tirantes": 0.0,
    "Manga Corta / Cap Sleeve": 25.0,
    "Manga 3/4 en Encaje": 45.0,
    "Manga Larga de Tul con Aplicaciones": 75.0,
    "Manga Abullonada / Bishop Sleeve": 60.0
}

ESTRUCTURA_INTERNA = {
    "Forro Estándar Suave": 30.0,
    "Corsé Interno con Varillas de Acero": 120.0,
    "Copas Estructuradas Integradas": 40.0,
    "Enagua / Cancán de Tul Multicapa": 70.0
}

DETALLES_EXTRA = {
    "Bordado en Pedrería Fina a Mano": 180.0,
    "Aplicaciones de Encaje Rebrodé": 110.0,
    "Plumas Naturales en Ruedo/Escote": 140.0,
    "Cola Real Desmontable (2 metros)": 160.0,
    "Cinturón con Cristales Swarovski": 85.0,
    "Velo Cathedral a Juego (3 metros)": 130.0
}

COSTO_BASE_MANO_OBRA = 200.0  # Base de patronaje y confección

# --- LAYOUT PRINCIPAL (2 COLUMNAS) ---
col_formulario, col_resumen = st.columns([1.6, 1], gap="large")

with col_formulario:
    st.subheader("🛠️ Configuración de la Prenda")
    
    # PESTAÑAS PASO A PASO
    tab_telas, tab_diseno, tab_detalles, tab_servicio = st.tabs([
        "1. 🧵 Materiales", 
        "2. ✂️ Silueta & Diseño", 
        "3. ✨ Detalles VIP", 
        "4. ⏱️ Tiempo & Pruebas"
    ])

    with tab_telas:
        st.markdown("##### Selección de Textiles y Estructura")
        tela_sel = st.selectbox("Tipo de Tela Principal:", list(TELAS.keys()))
        metros_sel = st.slider("Metros de tela requeridos:", min_value=2.0, max_value=12.0, value=4.5, step=0.5)
        
        st.markdown("---")
        st.markdown("##### Refuerzo y Corsetería Interna")
        estructura_sel = st.multiselect(
            "Acabados e Interiores:",
            list(ESTRUCTURA_INTERNA.keys()),
            default=["Forro Estándar Suave"]
        )

    with tab_diseno:
        st.markdown("##### Silueta y Cortes Principales")
        corte_col1, corte_col2 = st.columns(2)
        with corte_col1:
            silueta_sel = st.selectbox("Corte / Silueta:", list(SILUETAS.keys()))
            escote_sel = st.selectbox("Tipo de Escote:", list(ESCOTES.keys()))
        with corte_col2:
            espalda_sel = st.selectbox("Diseño de Espalda:", list(ESPALDAS.keys()))
            manga_sel = st.selectbox("Estilo de Mangas:", list(MANGAS.keys()))

    with tab_detalles:
        st.markdown("##### Aplicaciones y Adornos Hechos a Mano")
        detalles_sel = st.multiselect(
            "Selecciona los elementos decorativos adicionales:",
            list(DETALLES_EXTRA.keys())
        )

    with tab_servicio:
        st.markdown("##### Prioridad de Entrega y Experiencia")
        tiempo_entrega = st.radio(
            "Tiempo de Confección:",
            ["Estándar (6 - 8 Semanas)", "Prioritario (3 - 4 Semanas) [ +15% ]", "Express de Emergencia (1 - 2 Semanas) [ +30% ]"]
        )
        
        pruebas_sel = st.select_slider(
            "Número de Pruebas de Vestuario (Fittings):",
            options=["2 Pruebas (Incluidas)", "3 Pruebas (+ $40)", "5 Pruebas VIP con Diseñadora (+ $90)"]
        )

# --- CÁLCULOS DE PRECIOS ---
costo_materia_prima = TELAS[tela_sel] * metros_sel
costo_estructura = sum([ESTRUCTURA_INTERNA[item] for item in estructura_sel])
costo_diseno = SILUETAS[silueta_sel] + ESCOTES[escote_sel] + ESPALDAS[espalda_sel] + MANGAS[manga_sel]
costo_detalles = sum([DETALLES_EXTRA[item] for item in detalles_sel])

costo_pruebas = 0.0
if "3 Pruebas" in pruebas_sel:
    costo_pruebas = 40.0
elif "5 Pruebas" in pruebas_sel:
    costo_pruebas = 90.0

subtotal = COSTO_BASE_MANO_OBRA + costo_materia_prima + costo_estructura + costo_diseno + costo_detalles + costo_pruebas

# Multiplicador por tiempo de entrega
multiplicador_urgencia = 1.0
if "Prioritario" in tiempo_entrega:
    multiplicador_urgencia = 1.15
elif "Express" in tiempo_entrega:
    multiplicador_urgencia = 1.30

precio_total_final = subtotal * multiplicador_urgencia
recargo_urgencia_monto = precio_total_final - subtotal

# --- COLUMNA DE RESUMEN Y COTIZACIÓN ---
with col_resumen:
    st.subheader("📊 Cotización Oficial")
    
    # DATOS DE LA CLIENTA
    with st.expander("👤 Datos de la Clienta / Evento", expanded=True):
        nombre_clienta = st.text_input("Nombre de la Clienta:", value="María Fernanda López")
        tipo_evento = st.selectbox("Tipo de Evento:", ["Boda / Novia", "Gala / Copenhague", "Graduación VIP", "XV Años / Quinceañera", "Cocktail de Lujo"])

    st.markdown("---")
    
    # MÉTRICAS DESTACADAS
    st.metric(
        label="💰 PRECIO TOTAL ESTIMADO", 
        value=f"${precio_total_final:,.2f} USD",
        delta=f"+${recargo_urgencia_monto:,.2f} USD por Urgencia" if recargo_urgencia_monto > 0 else "Precio Estándar"
    )

    st.markdown("##### 📈 Desglose Técnico de Costos")
    
    # DATAFRAME PARA EL GRÁFICO Y TABLA
    df_desglose = pd.DataFrame({
        "Concepto": ["Confección Base", "Textil Principal", "Corsetería/Estructura", "Cortes y Diseño", "Bordados/Detalles", "Servicios/Pruebas"],
        "Costo (USD)": [COSTO_BASE_MANO_OBRA, costo_materia_prima, costo_estructura, costo_diseno, costo_detalles, costo_pruebas]
    })
    
    # GRÁFICO BARRAS STREAMLIT
    st.bar_chart(df_desglose.set_index("Concepto"))

    # DETALLE DESPLEGABLE
    with st.expander("🔍 Ver Desglose Detallado"):
        st.write(f"• **Confección Base:** ${COSTO_BASE_MANO_OBRA:.2f} USD")
        st.write(f"• **Tela ({tela_sel} x {metros_sel}m):** ${costo_materia_prima:.2f} USD")
        st.write(f"• **Corsetería/Forros:** ${costo_estructura:.2f} USD")
        st.write(f"• **Personalización de Diseño:** ${costo_diseno:.2f} USD")
        st.write(f"• **Bordados y Aplicaciones:** ${costo_detalles:.2f} USD")
        st.write(f"• **Pruebas de Ajuste:** ${costo_pruebas:.2f} USD")
        if recargo_urgencia_monto > 0:
            st.write(f"• **Tarifa de Confección Acelerada:** ${recargo_urgencia_monto:.2f} USD")

    # GENERAR ARCHIVO DE RESUMEN PARA DESCARGAR
    resumen_texto = f"""
    ==================================================
                 ATELIER VIRTUAL - COTIZACIÓN
    ==================================================
    Clienta: {nombre_clienta}
    Tipo de Evento: {tipo_evento}
    
    DETALLES DEL DISEÑO:
    - Tela: {tela_sel} ({metros_sel}m)
    - Silueta: {silueta_sel}
    - Escote: {escote_sel}
    - Espalda: {espalda_sel}
    - Mangas: {manga_sel}
    - Estructura Interna: {', '.join(estructura_sel) if estructura_sel else 'Ninguna'}
    - Adicionales: {', '.join(detalles_sel) if detalles_sel else 'Ninguno'}
    - Tiempo de Entrega: {tiempo_entrega}
    - Pruebas: {pruebas_sel}
    
    --------------------------------------------------
    DESGLOSE ECONÓMICO:
    - Confección Base: ${COSTO_BASE_MANO_OBRA:.2f} USD
    - Tela: ${costo_materia_prima:.2f} USD
    - Estructura/Forros: ${costo_estructura:.2f} USD
    - Diseño y Cortes: ${costo_diseno:.2f} USD
    - Detalles VIP: ${costo_detalles:.2f} USD
    - Pruebas/Fittings: ${costo_pruebas:.2f} USD
    - Recargo Urgencia: ${recargo_urgencia_monto:.2f} USD
    --------------------------------------------------
    PRECIO TOTAL ESTIMADO: ${precio_total_final:,.2f} USD
    ==================================================
    """

    st.download_button(
        label="📄 Descargar Cotización Oficial (.txt)",
        data=resumen_texto,
        file_name=f"Cotizacion_{nombre_clienta.replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
