"""Aplicacion Streamlit para convertir entre pies y metros."""

import math

import streamlit as st


FEET_TO_METERS = 0.3048


def convert_value(value: float, unit: str) -> tuple[float, str]:
    """Convierte un valor numerico desde la unidad de origen a su unidad opuesta."""
    if unit == "Pies":
        return value * FEET_TO_METERS, "metros"
    return value / FEET_TO_METERS, "pies"


st.set_page_config(page_title="Conversor de unidades", page_icon="📏")
st.title("Conversor de pies y metros")
st.write("Selecciona la unidad de origen, ingresa un número válido y obtén la conversión.")

if st.button("Salir"):
    st.info("Aplicación finalizada. Puedes cerrar la pestaña y detener Streamlit en la terminal.")
    st.stop()

unit = st.segmented_control(
    "Unidad de origen",
    options=["Pies", "Metros"],
    default="Pies",
    selection_mode="single",
)

value_text = st.text_input("Ingresa el valor a convertir", placeholder="Ejemplo: 12.5")

if st.button("Convertir"):
    try:
        value = float(value_text.strip())
        if not math.isfinite(value):
            raise ValueError
    except (ValueError, AttributeError):
        st.error("No es un valor válido. Ingresa un número real.")
    else:
        converted_value, target_unit = convert_value(value, unit or "Pies")
        source_unit = (unit or "Pies").lower()
        st.success(f"{value:.4f} {source_unit} equivalen a {converted_value:.4f} {target_unit}.")
