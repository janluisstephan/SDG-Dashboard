import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Daten laden mit Caching
@st.cache_data
def load_data():
    data_path = 'Data/SDR2024-data.xlsx'
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

# SDG-Labels vorbereiten
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

# Streamlit Layout
st.title("Sustainable Development Goals Dashboard")
st.subheader("Select an SDG to view country performance and trends.")

# Dropdown-Menü für SDG-Auswahl
selected_sdg_label = st.selectbox("Choose an SDG:", sdg_labels)
selected_sdg_index = sdg_labels.index(selected_sdg_label)
current_sdg = color_columns[selected_sdg_index]
current_trend = trend_columns[selected_sdg_index]

# Karten-Daten vorbereiten
filtered_data = color_data[["Country", current_sdg]].dropna()
filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

# Karte erstellen
fig = px.choropleth(
    filtered_data,
    locations="Country",
    locationmode="country names",
    color="Color",
    hover_name="Country",
    title="",
    color_discrete_map=color_mapping
)

# Margen und Hintergrund anpassen
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),  # Alle Margen entfernen
    paper_bgcolor="#f9f9f9",  # Hintergrundfarbe (optional)
    plot_bgcolor="#f9f9f9",   # Plot-Hintergrundfarbe (optional)
    showlegend=False,
    dragmode=False  # Karte statisch machen
)

# Layout mit zwei Spalten
col1, col2 = st.columns([5, 1])  # 83% für die Karte, 17% für die Legende

with col1:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.write("### Legend")
    st.write("This section is currently empty.")
