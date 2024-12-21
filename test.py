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
col1, col2, col3, col4 = st.columns(4)

for idx, label in enumerate(sdg_labels):
    image_path = os.path.join(sdg_images_path, f"{idx + 1}.png")
    col = [col1, col2, col3, col4][idx % 4]
    with col:
        if os.path.exists(image_path):
            if st.button(label, key=f"button_{idx}"):
                update_sdg(label)
            st.image(image_path, caption=label, use_column_width=True)
