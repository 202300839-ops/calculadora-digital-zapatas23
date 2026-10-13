import math
import streamlit as st

st.set_page_config(
    page_title="Calculadora digital de zapatas",
    page_icon="🏗️",
    layout="centered"
)

st.title("Calculadora digital para el diseño preliminar de zapatas")
st.caption("Predimensionamiento y selección preliminar de cimentación")
st.info(
    "Herramienta académica de predimensionamiento. Los resultados no sustituyen "
    "el diseño estructural definitivo ni las comprobaciones de punzonamiento, "
    "cortante, flexión, excentricidad y asentamientos."
)

st.header("1. Datos de entrada")

with st.form("formulario_calculo"):
    numero_columnas = st.number_input(
        "Número de columnas", min_value=1, max_value=100, value=1, step=1
    )
    carga_muerta = st.number_input(
        "Carga muerta por columna (kN)", min_value=0.0, value=500.0, step=10.0
    )
    carga_viva = st.number_input(
        "Carga viva por columna (kN)", min_value=0.0, value=150.0, step=10.0
    )
    distancia = st.number_input(
        "Distancia entre columnas (m)", min_value=0.0, value=3.0, step=0.1
    )
    posicion = st.selectbox(
        "Posición de la columna (aplicable a una columna)",
        ["Céntrica", "Excéntrica"]
    )
    qadm = st.number_input(
        "Presión admisible del suelo (kN/m²)",
        min_value=0.0, value=150.0, step=5.0
    )
    submitted = st.form_submit_button("Calcular predimensionamiento", type="primary")

if submitted:
    try:
        if carga_muerta + carga_viva <= 0:
            raise ValueError("La carga total debe ser mayor que cero.")
        if qadm <= 0:
            raise ValueError("La presión admisible debe ser mayor que cero.")
        if numero_columnas > 1 and distancia <= 0:
            raise ValueError(
                "Para dos o más columnas, la distancia entre columnas debe ser mayor que cero."
            )

        # Se conserva el procedimiento de cálculo del programa original.
        # IMPORTANTE: las cargas se interpretan como cargas por columna.
        carga_total = numero_columnas * (carga_muerta + carga_viva)

        if numero_columnas == 1:
            tipo_cimentacion = (
                "ZAPATA AISLADA" if posicion == "Céntrica"
                else "ZAPATA AISLADA EXCÉNTRICA"
            )
        elif numero_columnas == 2:
            tipo_cimentacion = "ZAPATA COMBINADA"
        else:
            tipo_cimentacion = "ZAPATA CORRIDA"

        area_requerida = carga_total / qadm

        if numero_columnas == 1:
            lado = math.ceil(math.sqrt(area_requerida) / 0.05) * 0.05
            largo = lado
            ancho = lado
        elif numero_columnas == 2:
            longitud_minima = distancia + 0.60
            largo = max(longitud_minima, math.sqrt(area_requerida))
            ancho = max(area_requerida / largo, 0.80)
            ancho = math.ceil(ancho / 0.05) * 0.05
            largo = max(area_requerida / ancho, longitud_minima)
            largo = math.ceil(largo / 0.05) * 0.05
        else:
            largo = (numero_columnas - 1) * distancia + 0.60
            ancho = max(area_requerida / largo, 0.60)
            ancho = math.ceil(ancho / 0.05) * 0.05

        area_adoptada = largo * ancho

        if numero_columnas == 1:
            altura = max(0.25, largo / 6)
        elif numero_columnas == 2:
            altura = max(0.30, ancho / 4)
        else:
            altura = max(0.25, ancho / 3)

        altura = min(altura, 0.60)
        altura = math.ceil(altura / 0.05) * 0.05

        st.header("2. Resultados del predimensionamiento")
        st.success(f"Tipo de cimentación recomendado: **{tipo_cimentacion}**")

        c1, c2 = st.columns(2)
        c1.metric("Carga total", f"{carga_total:,.2f} kN")
        c2.metric("Área requerida", f"{area_requerida:,.2f} m²")

        c3, c4 = st.columns(2)
        c3.metric("Largo preliminar", f"{largo:.2f} m")
        c4.metric("Ancho preliminar", f"{ancho:.2f} m")

        c5, c6 = st.columns(2)
        c5.metric("Área adoptada", f"{area_adoptada:.2f} m²")
        c6.metric("Altura preliminar", f"{altura:.2f} m")

        if area_adoptada >= area_requerida:
            st.success("Comprobación geométrica preliminar: el área adoptada es igual o mayor que el área requerida.")
        else:
            st.warning("El área adoptada resulta menor que el área requerida. Debe revisarse el dimensionamiento.")

        st.warning(
            "La selección y las dimensiones son preliminares. Esta versión conserva "
            "el método simplificado del código original y no verifica momentos, "
            "distribución real de cargas, presión no uniforme, punzonamiento, cortante, "
            "flexión ni asentamientos. Requiere revisión por un profesional estructural."
        )

    except (ValueError, OverflowError) as error:
        st.error(str(error))

st.divider()
st.caption("Calculadora académica de predimensionamiento de cimentaciones superficiales.")
