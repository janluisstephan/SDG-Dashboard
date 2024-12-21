import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Streamlit-Konfiguration
st.set_page_config(page_title="SDG Dashboard", layout="wide")

# Beispiel-Daten
sdg_labels = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]

sdg_images_path = 'assets'

# Session State initialisieren
if "selected_sdg" not in st.session_state:
    st.session_state["selected_sdg"] = sdg_labels[0]

def update_sdg(selected_sdg):
    st.session_state["selected_sdg"] = selected_sdg

# Kartenanzeige (Dummy-Beispiel)
st.header(f"Selected SDG: {st.session_state['selected_sdg']}")

# SDG-Schaltflächen mit Bildern
st.write("### Select an SDG:")

html_buttons = """
<div style="display: flex; flex-wrap: wrap; justify-content: center;">
"""

for idx, label in enumerate(sdg_labels):
    image_path = os.path.join(sdg_images_path, f"{idx + 1}.png")
    if os.path.exists(image_path):
        button_html = f"""
        <div style='text-align: center; margin: 10px;'>
            <form action="" method="get">
                <button type="submit" name="sdg" value="{label}" style="border: none; background: none; cursor: pointer;">
                    <img src="{image_path}" alt="{label}" style="width: 100px; height: auto;">
                </button>
            </form>
            <p style='color: black;'>{label}</p>
        </div>
        """
        html_buttons += button_html

html_buttons += "</div>"

st.markdown(html_buttons, unsafe_allow_html=True)

# SDG-Auswahl aktualisieren
query_params = st.experimental_get_query_params()
if "sdg" in query_params:
    selected_sdg = query_params["sdg"][0]
    update_sdg(selected_sdg)
