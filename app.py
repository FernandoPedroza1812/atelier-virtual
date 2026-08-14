import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from gradio_client import Client, handle_file
import tempfile
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Atelier Virtual | Cotizador & Probador IA",
    layout="wide",
    page_icon="👗"
)

# --- ESTILOS CSS PERSONALIZADOS ---
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

# --- ENCABEZADO ---
st.title("👗 Atelier Virtual: Cotizador & Probador IA")
st.caption("Plataforma profesional de diseño a la medida, cotización en tiempo real y prueba virtual con IA.")
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

# --- RESPALDO: DOSSIER DE DISEÑO ---
def crear_moodboard_profesional(foto_cliente_file, foto_vestido_file, clienta, tela, silueta):
    cliente_img = Image.open(foto_cliente_file).convert("RGB")
    vestido_img = Image.open(foto_vestido_file).convert("RGB")
    
    canvas_w, canvas_h = 1000, 650
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#111111")
    draw = ImageDraw.Draw(canvas)
    
    frame_w, frame_h = 420, 500
    cliente_crop = ImageOps.fit(cliente_img, (frame_w, frame_h), method=Image.Resampling.LANCZOS)
    vestido_crop = ImageOps.fit(vestido_img, (frame_w, frame_h), method=Image.Resampling.LANCZOS)
    
    canvas.paste(cliente_crop, (50, 90))
    canvas.paste(vestido_crop, (530, 90))
    
    draw.rectangle([(48, 88), (472, 592)], outline="#D4AF37", width=2)
    draw.rectangle([(528, 88), (952, 592)], outline="#D4AF37", width=2)
    
    draw.text((50, 35), "ATELIER HAUTE COUTURE — VISUAL DOSSIER", fill="#FFFFFF")
    draw.text((530, 35), f"CLIENTA: {clienta.upper()}", fill="#D4AF37")
    draw.text((65, 565), "PERFIL BASE", fill="#E0E0E0")
    draw.text((545, 565), f"PRENDA: {silueta.split('/')[0]}", fill="#E0E0E0")
    
    return canvas

# --- LAYOUT PRINCIPAL ---
col_formulario, col_resumen = st.columns([1.5, 1], gap="large")

with col_formulario:
    st.subheader("🛠️ Personalización & Configuración")
    
    tab_telas, tab_diseno, tab_detalles, tab_servicio, tab_probador = st.tabs([
        "1. 🧵 Materiales", 
        "2. ✂️ Silueta", 
        "3. ✨ Detalles VIP", 
        "4. ⏱️ Tiempo",
        "5. 📸 Probador Virtual"
    ])

    with tab_telas:
        st.markdown("##### Selección de Textiles y Estructura")
        tela_sel = st.selectbox("Tipo de Tela Principal:", list(TELAS.keys()))
        metros_sel = st.slider("Metros de tela requeridos:", 2.0, 12.0, 4.5, 0.5)
        estructura_sel = st.multiselect("Acabados e Interiores:", list(ESTRUCTURA_INTERNA.keys()), default=["Forro Estándar Suave"])

    with tab_diseno:
        st.markdown("##### Silueta, Escote y Cortes")
        c1, c2 = st.columns(2)
        with c1:
            silueta_sel = st.selectbox("Corte / Silueta:", list(SILUETAS.keys()))
            escote_sel = st.selectbox("Tipo de Escote:", list(ESCOTES.keys()))
        with c2:
            espalda_sel = st.selectbox("Diseño de Espalda:", list(ESPALDAS.keys()))
            manga_sel = st.selectbox("Estilo de Mangas:", list(MANGAS.keys()))

    with tab_detalles:
        st.markdown("##### Aplicaciones y Adornos Hechos a Mano")
        detalles_sel = st.multiselect("Selecciona los elementos decorativos:", list(DETALLES_EXTRA.keys()))

    with tab_servicio:
        st.markdown("##### Prioridad de Entrega y Experiencia")
        tiempo_entrega = st.radio("Tiempo de Confección:", ["Estándar (6 - 8 Semanas)", "Prioritario (3 - 4 Semanas) [ +15% ]", "Express de Emergencia (1 - 2 Semanas) [ +30% ]"])
        pruebas_sel = st.select_slider("Pruebas de Vestuario (Fittings):", options=["2 Pruebas (Incluidas)", "3 Pruebas (+ $40)", "5 Pruebas VIP (+ $90)"])

    with tab_probador:
        st.markdown("##### Cargar Imágenes para IA (IDM-VTON)")
        foto_cliente = st.file_uploader("1. Foto de la Persona (Cuerpo entero)", type=["jpg", "png", "jpeg"])
        foto_vestido = st.file_uploader("2. Foto de la Prenda / Vestido", type=["jpg", "png", "jpeg"])

# --- CÁLCULOS DE PRECIOS ---
costo_materia_prima = TELAS[tela_sel] * metros_sel
costo_estructura = sum([ESTRUCTURA_INTERNA[item] for item in estructura_sel])
costo_diseno = SILUETAS[silueta_sel] + ESCOTES[escote_sel] + ESPALDAS[espalda_sel] + MANGAS[manga_sel]
costo_detalles = sum([DETALLES_EXTRA[item] for item in detalles_sel])

costo_pruebas = 40.0 if "3 Pruebas" in pruebas_sel else (90.0 if "5 Pruebas" in pruebas_sel else 0.0)
subtotal = COSTO_BASE_MANO_OBRA + costo_materia_prima + costo_estructura + costo_diseno + costo_detalles + costo_pruebas

multiplicador_urgencia = 1.15 if "Prioritario" in tiempo_entrega else (1.30 if "Express" in tiempo_entrega else 1.0)
precio_total_final = subtotal * multiplicador_urgencia
recargo_urgencia_monto = precio_total_final - subtotal

# --- COLUMNA DERECHA: RESUMEN Y PROBADOR IA ---
with col_resumen:
    st.subheader("📊 Resultados & Cotización")
    
    with st.expander("👤 Datos de la Clienta / Evento", expanded=True):
        nombre_clienta = st.text_input("Nombre de la Clienta:", value="María Fernanda López")
        tipo_evento = st.selectbox("Tipo de Evento:", ["Boda / Novia", "Gala VIP", "Graduación", "XV Años", "Cocktail"])

    st.markdown("---")
    
    st.metric(
        label="💰 PRECIO TOTAL ESTIMADO", 
        value=f"${precio_total_final:,.2f} USD",
        delta=f"+${recargo_urgencia_monto:,.2f} USD por Urgencia" if recargo_urgencia_monto > 0 else "Precio Estándar"
    )

    # BOTÓN DE PROBADOR VIRTUAL CON IA REAL
    btn_generar = st.button("✨ Generar Probador Virtual con IA", use_container_width=True, type="primary")
    
    if btn_generar:
        if not foto_cliente or not foto_vestido:
            st.warning("⚠️ Sube la foto de la persona y la foto del vestido en la pestaña '5. Probador Virtual'.")
        else:
            with st.spinner("Procesando prueba virtual con IA en servidor Hugging Face (~15 seg)..."):
                exito_ia = False
                
                # Crear archivos temporales
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f_model:
                    f_model.write(foto_cliente.getvalue())
                    model_path = f_model.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f_garm:
                    f_garm.write(foto_vestido.getvalue())
                    garm_path = f_garm.name

                try:
                    # Llamada a la IA gratuita de IDM-VTON
                    client = Client("yisol/IDM-VTON")
                    result = client.predict(
                        dict={"background": handle_file(model_path), "layers": [], "composite": None},
                        garm_img=handle_file(garm_path),
                        garment_des="dress",
                        is_checked=True,
                        is_checked_crop=False,
                        denoise_steps=30,
                        seed=42,
                        api_name="/tryon"
                    )
                    
                    output_image_path = result[0]
                    final_image = Image.open(output_image_path)
                    st.image(final_image, caption="✨ Probador Virtual con IA Generativa (IDM-VTON)", use_container_width=True)
                    st.success("¡Imagen generada con éxito por la IA!")
                    exito_ia = True

                except Exception as e:
                    exito_ia = False

                finally:
                    if os.path.exists(model_path): os.remove(model_path)
                    if os.path.exists(garm_path): os.remove(garm_path)

                # Si el servidor gratuito de IA está saturation/ocupado, genera el dossier elegante
                if not exito_ia:
                    foto_cliente.seek(0)
                    foto_vestido.seek(0)
                    moodboard = crear_moodboard_profesional(foto_cliente, foto_vestido, nombre_clienta, tela_sel, silueta_sel)
                    st.image(moodboard, caption="✨ Dossier de Diseño & Comparativa Técnica", use_container_width=True)
                    st.info("ℹ️ *Se desplegó la Ficha Técnica debido a alta demanda en los servidores de IA.*")

    st.markdown("---")
    st.markdown("##### 📈 Distribución de Costos")
    
    df_desglose = pd.DataFrame({
        "Concepto": ["Confección", "Textil", "Corsetería", "Diseño", "Detalles VIP", "Pruebas"],
        "Costo (USD)": [COSTO_BASE_MANO_OBRA, costo_materia_prima, costo_estructura, costo_diseno, costo_detalles, costo_pruebas]
    })
    st.bar_chart(df_desglose.set_index("Concepto"))

    with st.expander("🔍 Ver Desglose Detallado"):
        st.write(f"• **Confección Base:** ${COSTO_BASE_MANO_OBRA:.2f} USD")
        st.write(f"• **Tela ({tela_sel}):** ${costo_materia_prima:.2f} USD")
        st.write(f"• **Corsetería:** ${costo_estructura:.2f} USD")
        st.write(f"• **Cortes/Diseño:** ${costo_diseno:.2f} USD")
        st.write(f"• **Bordados/Detalles:** ${costo_detalles:.2f} USD")
        st.write(f"• **Pruebas:** ${costo_pruebas:.2f} USD")

    # DESCARGAR COTIZACIÓN
    resumen_texto = f"""
    ==================================================
                 ATELIER VIRTUAL - COTIZACIÓN
    ==================================================
    Clienta: {nombre_clienta} | Evento: {tipo_evento}
    
    DETALLES DEL DISEÑO:
    - Tela: {tela_sel} ({metros_sel}m)
    - Silueta: {silueta_sel} | Escote: {escote_sel}
    - Espalda: {espalda_sel} | Mangas: {manga_sel}
    - Entrega: {tiempo_entrega} | Fittings: {pruebas_sel}
    
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
