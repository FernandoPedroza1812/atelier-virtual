import streamlit as st
import pandas as pd
import replicate
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Atelier Virtual - Cotizador & IA", layout="wide", page_icon="👗")

st.title("👗 Atelier Virtual: Personalización & Probador con IA")
st.write("Prototipo interactivo de diseño de prendas a la medida y visualización en tiempo real.")

# --- BASE DE DATOS DE PRECIOS ---
PRECIOS_TELAS = {
    "Seda de Mora": 45.0,
    "Raso Satinado": 25.0,
    "Encaje Francés": 60.0,
    "Tul Bordado": 35.0,
    "Algodón Lino": 18.0
}

COSTO_BASE_CONFECCION = 150.0

# --- ESTRUCTURA EN COLUMNAS ---
col_controles, col_visualizador = st.columns([1, 1])

with col_controles:
    st.header("1. Personaliza tu Vestido")
    
    tela_seleccionada = st.selectbox("Selecciona la Tela:", list(PRECIOS_TELAS.keys()))
    metros_tela = st.slider("Metros de tela estimados:", min_value=2.0, max_value=8.0, value=3.5, step=0.5)
    
    corte = st.selectbox("Tipo de Corte / Silueta:", ["A-Line", "Sirena", "Princesa", "Recto"])
    escote = st.selectbox("Tipo de Escote:", ["Corazón", "En V", "Bandeau", "Cuello Alto"])
    
    detalles_extra = st.multiselect(
        "Detalles Adicionales:",
        ["Pedrería (+$80)", "Manga Larga (+$40)", "Cola Larga (+$50)"]
    )

    # Lógica de Precios
    costo_tela = PRECIOS_TELAS[tela_seleccionada] * metros_tela
    costo_extras = sum([80 if "Pedrería" in d else 40 if "Manga" in d else 50 for d in detalles_extra])
    precio_total = COSTO_BASE_CONFECCION + costo_tela + costo_extras

    st.markdown("---")
    st.subheader("💰 Cotización en Tiempo Real")
    st.metric(label="Precio Total Estimado", value=f"${precio_total:.2f} USD")
    
    with st.expander("Ver desglose del precio"):
        st.write(f"- Confección base: **${COSTO_BASE_CONFECCION:.2f} USD**")
        st.write(f"- Tela ({tela_seleccionada} x {metros_tela}m): **${costo_tela:.2f} USD**")
        st.write(f"- Adicionales: **${costo_extras:.2f} USD**")

with col_visualizador:
    st.header("2. Probador Virtual (IA)")
    
    # Interruptor para el modo Demo/A prueba de fallos
    modo_demo = st.toggle("🧪 Activar Modo Demo (Simulación rápida para presentación)", value=False)
    
    foto_cliente = st.file_uploader("Sube la foto de la clienta", type=["jpg", "png", "jpeg"])
    foto_vestido = st.file_uploader("Sube la foto/diseño del vestido", type=["jpg", "png", "jpeg"])
    
    default_token = st.secrets.get("REPLICATE_API_TOKEN", "")
    api_key = st.text_input("Replicate API Token:", value=default_token, type="password")

    if st.button("✨ Generar Visualización con IA", use_container_width=True):
        if modo_demo:
            # MODO DEMO: Genera un resultado instantáneo sin consumir la API
            with st.spinner("Procesando renderizado de la prenda... (~2 segundos)"):
                time.sleep(2)
                # Imagen de muestra de Virtual Try-On
                st.image(
                    "https://raw.githubusercontent.com/yisol/IDM-VTON/main/assets/examples/result_0.png", 
                    caption="Resultado del Probador Virtual (Simulado para Presentación)", 
                    use_container_width=True
                )
                st.success("¡Visualización completada con éxito!")
        else:
            # MODO REAL: Llama a la API de Replicate
            if not foto_cliente or not foto_vestido:
                st.warning("⚠️ Por favor sube ambas imágenes (Clienta y Vestido).")
            elif not api_key:
                st.error("🔑 Ingresa un API Token de Replicate para continuar.")
            else:
                with st.spinner("Procesando imagen con IA en la nube... (~10 segundos)"):
                    try:
                        client = replicate.Client(api_token=api_key)
                        output = client.run(
                            "yisol/idm-vton:c871d0b19165cb70e7db9294191653f5383501f2e82f3c2f0f49f80a480572b8",
                            input={
                                "human_img": foto_cliente,
                                "garm_img": foto_vestido,
                                "description": f"A {corte} dress with {escote} neckline, made of {tela_seleccionada}"
                            }
                        )
                        st.image(output, caption="Resultado del Probador Virtual con IA", use_container_width=True)
                        st.success("¡Visualización completada con éxito!")
                    except Exception as e:
                        st.error("⚠️ El servidor de la IA está saturado en la cuenta gratuita.")
                        st.info("💡 Tip: Activa el botón 'Modo Demo' arriba para mostrar el resultado sin interrupciones.")
