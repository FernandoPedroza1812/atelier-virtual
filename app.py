import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageOps

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Atelier Virtual | Cotizador & Dossier de Diseño",
    layout="wide",
    page_icon="👗"
)

# --- ESTILOS CSS PERSONALIZADOS (ESTÉTICA DE LUJO) ---
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #eaeaea;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
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
st.title("👗 Atelier Virtual: Cotizador & Dossier de Diseño")
st.caption("Plataforma profesional de diseño a la medida, cotización en tiempo real y fichas técnicas de visualización.")
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

COSTO_BASE_MANO_OBRA = 200.0

# --- GENERADOR DE DOSSIER EDITORIAL / FICHA TÉCNICA ---
def crear_dossier_profesional(foto_cliente_file, foto_vestido_file, clienta, tela, silueta, escote):
    cliente_img = Image.open(foto_cliente_file).convert("RGB")
    vestido_img = Image.open(foto_vestido_file).convert("RGB")
    
    # Dimensiones del lienzo
    canvas_w, canvas_h = 1000, 650
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#111111")
    draw = ImageDraw.Draw(canvas)
    
    # Procesar imágenes en marcos cuadrados/verticales estilizados
    frame_w, frame_h = 420, 500
    cliente_crop = ImageOps.fit(cliente_img, (frame_w, frame_h), method=Image.Resampling.LANCZOS)
    vestido_crop = ImageOps.fit(vestido_img, (frame_w, frame_h), method=Image.Resampling.LANCZOS)
    
    # Pegar imágenes lado a lado con margen editorial
    canvas.paste(cliente_crop, (50, 90))
    canvas.paste(vestido_crop, (530, 90))
    
    # Dibujar marcos de lujo dorados
    draw.rectangle([(48, 88), (472, 592)], outline="#D4AF37", width=2)
    draw.rectangle([(528, 88), (952, 592)], outline="#D4AF37", width=2)
    
    # Encabezados
    draw.text((50, 35), "ATELIER HAUTE COUTURE — VISUAL DOSSIER", fill="#FFFFFF")
    draw.text((530, 35), f"CLIENTA: {clienta.upper()}", fill="#D4AF37")
    
    # Etiquetas en pie de foto
    draw.rectangle([(50, 555), (470, 590)], fill=(0, 0, 0, 180))
    draw.rectangle([(530, 555), (950, 590)], fill=(0, 0, 0, 180))
    
    draw.text((65, 565), "PERFIL Y SILUETA BASE", fill="#E0E0E0")
    draw.text((545, 565), f"PRENDA: {silueta.split('/')[0]}", fill="#E0E0E0")
    
    # Pie de página técnico
    draw.text((50, 612), f"Textil: {tela}  |  Silueta: {silueta}  |  Escote: {escote}", fill="#888888")
    
    return canvas

# --- LAYOUT PRINCIPAL (2 COLUMNAS) ---
col_formulario, col_resumen = st.columns([1.5, 1], gap="large")

with col_formulario:
    st.subheader("🛠️ Personalización & Configuración")
    
    tab_telas, tab_diseno, tab_detalles, tab_servicio, tab_probador = st.tabs([
        "1. 🧵 Materiales", 
        "2. ✂️ Silueta", 
        "3. ✨ Detalles VIP", 
        "4. ⏱️ Tiempo",
        "5. 📸 Dossier Visual"
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
        st.markdown("##### Silueta, Escote y Cortes")
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

    with tab_probador:
        st.markdown("##### Fotos de Referencia para Ficha Técnica")
        foto_cliente = st.file_uploader("1. Foto de la Clienta / Modelo", type=["jpg", "png", "jpeg"])
        foto_vestido = st.file_uploader("2. Foto de Referencia de la Prenda", type=["jpg", "png", "jpeg"])

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

multiplicador_urgencia = 1.0
if "Prioritario" in tiempo_entrega:
    multiplicador_urgencia = 1.15
elif "Express" in tiempo_entrega:
    multiplicador_urgencia = 1.30

precio_total_final = subtotal * multiplicador_urgencia
recargo_urgencia_monto = precio_total_final - subtotal

# --- COLUMNA DE RESUMEN & VISUALIZACIÓN ---
with col_resumen:
    st.subheader("📊 Resultados & Cotización")
    
    # DATOS DE LA CLIENTA
    with st.expander("👤 Datos de la Clienta / Evento", expanded=True):
        nombre_clienta = st.text_input("Nombre de la Clienta:", value="María Fernanda López")
        tipo_evento = st.selectbox("Tipo de Evento:", ["Boda / Novia", "Gala VIP", "Graduación", "XV Años / Quinceañera", "Cocktail de Lujo"])

    st.markdown("---")
    
    # MÉTRICA DE PRECIO TOTAL
    st.metric(
        label="💰 PRECIO TOTAL ESTIMADO", 
        value=f"${precio_total_final:,.2f} USD",
        delta=f"+${recargo_urgencia_monto:,.2f} USD por Urgencia" if recargo_urgencia_monto > 0 else "Precio Estándar"
    )

    # BOTÓN PARA GENERAR EL DOSSIER VISUAL
    btn_generar = st.button("✨ Generar Ficha Técnica & Dossier Visual", use_container_width=True, type="primary")
    
    if btn_generar:
        if not foto_cliente or not foto_vestido:
            st.warning("⚠️ Ve a la pestaña '5. Dossier Visual' y sube la foto de la clienta y de la prenda.")
        else:
            with st.spinner("Procesando dossier de diseño..."):
                foto_cliente.seek(0)
                foto_vestido.seek(0)
                dossier_img = crear_dossier_profesional(
                    foto_cliente, foto_vestido, nombre_clienta, tela_sel, silueta_sel, escote_sel
                )
                st.image(dossier_img, caption="✨ Dossier de Diseño & Comparativa Técnica (Atelier Suite)", use_container_width=True)
                st.success("¡Ficha técnica generada con éxito!")

    st.markdown("---")
    st.markdown("##### 📈 Distribución de Costos")
    
    # GRÁFICO DE BARRAS DE COSTOS
    df_desglose = pd.DataFrame({
        "Concepto": ["Confección", "Textil", "Corsetería", "Cortes/Diseño", "Detalles VIP", "Pruebas"],
        "Costo (USD)": [COSTO_BASE_MANO_OBRA, costo_materia_prima, costo_estructura, costo_diseno, costo_detalles, costo_pruebas]
    })
    st.bar_chart(df_desglose.set_index("Concepto"))

    # DESGLOSE DESPLEGABLE
    with st.expander("🔍 Ver Desglose Detallado"):
        st.write(f"• **Confección Base:** ${COSTO_BASE_MANO_OBRA:.2f} USD")
        st.write(f"• **Tela ({tela_sel} x {metros_sel}m):** ${costo_materia_prima:.2f} USD")
        st.write(f"• **Corsetería/Forros:** ${costo_estructura:.2f} USD")
        st.write(f"• **Personalización de Diseño:** ${costo_diseno:.2f} USD")
        st.write(f"• **Bordados y Aplicaciones:** ${costo_detalles:.2f} USD")
        st.write(f"• **Pruebas de Ajuste:** ${costo_pruebas:.2f} USD")
        if recargo_urgencia_monto > 0:
            st.write(f"• **Tarifa de Confección Acelerada:** ${recargo_urgencia_monto:.2f} USD")

    # DESCARGAR COTIZACIÓN
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
