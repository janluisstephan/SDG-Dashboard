import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from io import BytesIO

# GitHub-Datenquelle
GITHUB_URL = "https://raw.githubusercontent.com/<username>/<repository>/main/SDR2024-data.xlsx"

# Daten laden
try:
    response = requests.get(GITHUB_URL)
    response.raise_for_status()  # Überprüft auf HTTP-Fehler
    data = BytesIO(response.content)

    sdg_data = pd.read_excel(data, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data, sheet_name='Overview', engine='openpyxl')

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
    color_meanings = {
        "green": "Goal Achievement",
        "yellow": "Challenges remain",
        "orange": "Significant challenges",
        "red": "Major challenges",
        "grey": "Insufficient data"
    }

    # Streamlit-Anwendung erstellen
    st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")
    st.title("🌍 Sustainable Development Goals Dashboard")

    # Initial SDG-Index
    initial_sdg_index = 0
    current_sdg = color_columns[initial_sdg_index]
    current_trend = trend_columns[initial_sdg_index]

    # SDG-Auswahl
    selected_sdg_index = st.selectbox("Select an SDG to view:", range(len(sdg_labels)), format_func=lambda x: sdg_labels[x])
    current_sdg = color_columns[selected_sdg_index]
    current_trend = trend_columns[selected_sdg_index]

    # Karte aktualisieren
    filtered_data = color_data[["Country", current_sdg]].dropna()
    filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

    fig = px.choropleth(
        filtered_data,
        locations="Country",
        locationmode="country names",
        color="Color",
        hover_name="Country",
        title=f"{sdg_labels[selected_sdg_index]}",
        color_discrete_map=color_mapping
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor="#f9f9f9", plot_bgcolor="#f9f9f9")

    st.plotly_chart(fig, use_container_width=True)

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

except requests.exceptions.RequestException as e:
    st.error(f"Fehler beim Laden der Datei: {e}")
