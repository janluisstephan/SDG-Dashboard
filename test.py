import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Streamlit-Anwendung konfigurieren (muss der erste Befehl sein)
st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")

# Daten laden
data_path = 'Data/SDR2024-data.xlsx'
sdg_images_path = 'assets/'

# Daten cachen, um Ladezeiten zu reduzieren
@st.cache_data
def load_data():
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')
    return sdg_data, color_data

sdg_data, color_data = load_data()

# SDG-Spalten identifizieren
sdg_columns = [col for col in sdg_data.columns if "Goal" in col and "Score" in col]
color_columns = [col for col in color_data.columns if col.startswith("SDG")]

# Dynamische Identifikation der Trendspalten
trend_columns = [
    color_data.columns[color_data.columns.get_loc(col) + 1] if color_data.columns.get_loc(col) + 1 < len(color_data.columns) else None
    for col in color_columns
]

# SDG-Labels vorbereiten (nur gültige Labels berücksichtigen)
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

# Farbcodierungen und Bedeutungen
color_mapping = {
    "green": "#2ca02c",
    "yellow": "#ffdd57",
    "orange": "#ffa500",
    "red": "#d62728",
    "grey": "#808080"
}
color_meanings = {
    "green": "Goal Achievement",
    "yellow": "Challenges remain",
    "orange": "Significant challenges",
    "red": "Major challenges",
    "grey": "Insufficient data"
}

st.title("🌍 Sustainable Development Goals Dashboard")

# Alle Karten vorbereiten und cachen
@st.cache_data
def prepare_all_figures():
    figures = {}
    valid_labels = []
    for idx, sdg in enumerate(color_columns):
        if idx >= len(sdg_labels):
            break
        filtered_data = color_data[["Country", sdg]].dropna()
        filtered_data.rename(columns={sdg: "Color"}, inplace=True)

        fig = px.choropleth(
            filtered_data,
            locations="Country",
            locationmode="country names",
            color="Color",
            hover_name="Country",
            title=f"{sdg_labels[idx]}",
            color_discrete_map=color_mapping
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor="#f9f9f9", plot_bgcolor="#f9f9f9")
        figures[sdg_labels[idx]] = fig
        valid_labels.append(sdg_labels[idx])
    return figures, valid_labels

all_figures, valid_sdg_labels = prepare_all_figures()

# SDG-Auswahl
selected_sdg_label = st.selectbox("Select an SDG to view:", valid_sdg_labels)
st.plotly_chart(all_figures[selected_sdg_label], use_container_width=True)

# Legende
st.write("### Legend")
st.markdown(
    """
    - **Green:** Goal Achievement  
    - **Yellow:** Challenges remain  
    - **Orange:** Significant challenges  
    - **Red:** Major challenges  
    - **Grey:** Insufficient data  
    """
)

# Trends
st.write("### Trend Explanation")
st.markdown(
    """
    - **↑ On track or maintaining achievement**  
    - **➚ Moderately Increasing**  
    - **→ Stagnating**  
    - **↓ Decreasing**  
    """
)
