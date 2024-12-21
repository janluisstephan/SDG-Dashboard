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

# HTML-Schaltflächen mit JavaScript
html_code = """
<div style="display: flex; flex-wrap: wrap; justify-content: center;">
"""

for idx, label in enumerate(sdg_labels):
    image_path = f"{sdg_images_path}/{idx + 1}.png"
    html_code += f"""
    <div style="text-align: center; margin: 10px;">
        <img src="{image_path}" alt="{label}" style="width: 100px; cursor: pointer;" onclick="updateSDG('{label}')">
        <p style="color: black;">{label}</p>
    </div>
    """

html_code += """
</div>
<script>
    function updateSDG(selectedSDG) {{
        const streamlitCustomEvent = new Event("streamlit_event");
        streamlitCustomEvent.data = {{ "sdg": selectedSDG }};
        document.dispatchEvent(streamlitCustomEvent);
    }}
</script>
"""

st.markdown(html_code, unsafe_allow_html=True)

# JavaScript-Ereignis-Listener registrieren
selected_sdg = st.session_state["selected_sdg"]
selected_sdg_js = st.text_input("Current SDG (JavaScript Event):", value=selected_sdg, key="sdg_js")

if selected_sdg_js != st.session_state["selected_sdg"]:
    update_sdg(selected_sdg_js)
