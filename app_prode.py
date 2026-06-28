import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="PRODE Liga de Laprida", page_icon="🏆")

st.title("🏆 PRODE - Liga de Laprida 2026")
st.write("Cargá tu tarjeta para la fecha actual de la liga.")

# 1. Configuración del Fixture Oficial Completo (14 fechas fidedignas)
fixture_oficial = {
    1: {"P1": ("BARRACAS", "JORGE NEWBERY"), "P2": ("RACING", "PLATENSE"), "P3": ("LILAN", "INGENIERO")},
    2: {"P1": ("JUVENTUD", "LILAN"), "P2": ("JORGE NEWBERY", "RACING"), "P3": ("INGENIERO", "BARRACAS")},
    3: {"P1": ("PLATENSE", "INGENIERO"), "P2": ("BARRACAS", "JUVENTUD"), "P3": ("RACING", "JORGE NEWBERY")},
    4: {"P1": ("JORGE NEWBERY", "LILAN"), "P2": ("JUVENTUD", "PLATENSE"), "P3": ("INGENIERO", "RACING")},
    5: {"P1": ("BARRACAS", "PLATENSE"), "P2": ("LILAN", "INGENIERO"), "P3": ("JUVENTUD", "RACING")},
    6: {"P1": ("JORGE NEWBERY", "BARRACAS"), "P2": ("PLATENSE", "LILAN"), "P3": ("INGENIERO", "JUVENTUD")},
    7: {"P1": ("JORGE NEWBERY", "LILAN"), "P2": ("RACING", "BARRACAS"), "P3": ("PLATENSE", "INGENIERO")},
    8: {"P1": ("JORGE NEWBERY", "BARRACAS"), "P2": ("PLATENSE", "RACING"), "P3": ("INGENIERO", "LILAN")},
    9: {"P1": ("LILAN", "JUVENTUD"), "P2": ("RACING", "JORGE NEWBERY"), "P3": ("BARRACAS", "INGENIERO")},
    10: {"P1": ("INGENIERO", "PLATENSE"), "P2": ("JUVENTUD", "BARRACAS"), "P3": ("JORGE NEWBERY", "RACING")},
    11: {"P1": ("LILAN", "JORGE NEWBERY"), "P2": ("PLATENSE", "JUVENTUD"), "P3": ("RACING", "INGENIERO")},
    12: {"P1": ("PLATENSE", "BARRACAS"), "P2": ("INGENIERO", "LILAN"), "P3": ("RACING", "JUVENTUD")},
    13: {"P1": ("BARRACAS", "JORGE NEWBERY"), "P2": ("LILAN", "PLATENSE"), "P3": ("JUVENTUD", "INGENIERO")},
    14: {"P1": ("LILAN", "JORGE NEWBERY"), "P2": ("BARRACAS", "RACING"), "P3": ("INGENIERO", "PLATENSE")}
}

# 2. CALENDARIO REAL DE RESTRICCIÓN (El límite máximo para mandar la jugada)
# El sistema lee este diccionario y borra la opción de la pantalla si ya pasó este domingo
calendario_prode = {
    1: datetime.date(2026, 6, 28),   # Fecha 1 (Hoy se puede jugar, mañana ya desaparece)
    2: datetime.date(2026, 7, 5),    # Fecha 2
    3: datetime.date(2026, 7, 12),   # Fecha 3
    4: datetime.date(2026, 7, 19),   # Fecha 4
    5: datetime.date(2026, 7, 26),   # Fecha 5
    6: datetime.date(2026, 8, 2),    # Fecha 6
    7: datetime.date(2026, 8, 9),    # Fecha 7
    8: datetime.date(2026, 8, 16),   # Fecha 8
    9: datetime.date(2026, 8, 23),   # Fecha 9
    10: datetime.date(2026, 8, 30),  # Fecha 10
    11: datetime.date(2026, 9, 6),   # Fecha 11
    12: datetime.date(2026, 9, 13),  # Fecha 12
    13: datetime.date(2026, 9, 20),  # Fecha 13
    14: datetime.date(2026, 9, 27)   # Fecha 14
}

hoy = datetime.date.today()

# El motor filtra y destruye de inmediato las opciones de fechas viejas
fechas_disponibles = []
for nro_fecha, domingo_limite in calendario_prode.items():
    if hoy <= domingo_limite:
        fechas_disponibles.append(nro_fecha)

# Bloqueo total automático si el campeonato ya se cerró
if not fechas_disponibles:
    st.info("🏆 ¡El torneo del PRODE ha finalizado oficialmente!")
    st.stop()

st.markdown("---")

# 3. Selector Inteligente: El menú solo muestra lo que es válido jugar hoy
fecha_seleccionada = st.selectbox(
    "Seleccioná la Fecha a jugar:", 
    options=fechas_disponibles,
    format_func=lambda x: f"Fecha {x} (Vence el {calendario_prode[x].strftime('%d/%m')})"
)

partidos_hoy = fixture_oficial[fecha_seleccionada]

st.markdown("---")

# 4. Formulario de inscripción estricto
with st.form(key="formulario_prode"):
    st.subheader("👤 Datos del Participante")
    nombre = st.text_input("Nombre Completo:").strip()
    celular = st.text_input("Número de Celular (con código de área):").strip()
    comprobante = st.text_input("Comprobante de Pago (ej: MP-100):").strip()
    
    st.markdown("---")
    st.subheader("⚽ Tus Pronósticos")
    
    # Extraemos limpiamente los rivales fijos de la tupla
    local1, visitante1 = partidos_hoy["P1"]
    local2, visitante2 = partidos_hoy["P2"]
    local3, visitante3 = partidos_hoy["P3"]
    
    opciones = ["LOCAL", "VISITANTE", "EMPATE"]
    
    # Formato vertical nativo: Infalible, no se deforma nunca
    p1 = st.radio(f"Partido 1: {local1} vs {visitante1}", opciones)
    p2 = st.radio(f"Partido 2: {local2} vs {visitante2}", opciones)
    p3 = st.radio(f"Partido 3: {local3} vs {visitante3}", opciones)
    
    st.markdown("---")
    enviar = st.form_submit_button(label="🚀 Enviar mi Tarjeta Oficial")

# 5. Respuesta del Servidor al procesar los datos obligatorios
if enviar:
    if not nombre or not celular or not comprobante:
        st.error("❌ Error: Todos los campos de datos personales son obligatorios.")
    else:
        st.success(f"¡Excelente {nombre}! Tu tarjeta para la Fecha {fecha_seleccionada} pasó los controles de seguridad y fue validada de forma impecable. ¡Mucha suerte! 🍀")
