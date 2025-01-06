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

# Karten-Daten vorbereiten
def generate_map(selected_sdg_index):
    current_sdg = color_columns[selected_sdg_index]
    filtered_data = color_data[["Country", current_sdg]].dropna()
    filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

    fig = px.choropleth(
        filtered_data,
        locations="Country",
        locationmode="country names",
        color="Color",
        hover_name="Country",
        title="",
        color_discrete_map=color_mapping
    )

    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#f9f9f9",
        plot_bgcolor="#f9f9f9",
        showlegend=False,
        dragmode=False
    )
    return fig

# Obere Zeile: Instructions, Map, Legend
col1, col2, col3 = st.columns([1.5, 4, 1.5])  # Adjust column proportions

# Instructions
with col1:
    st.markdown("## Instructions")
    st.write("""
    1. Select an SDG using the buttons below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Refer to the legend on the right to interpret the colors and trends.
    """)

# Map Placeholder
with col2:
    st.write("### Global SDG Performance")
    map_placeholder = st.empty()

# Legend
with col3:
    st.markdown("## Legend")
    st.markdown("### Colors")
    for color, hex_value in color_mapping.items():
        st.markdown(f"<div style='background-color: {hex_value}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;'></div> {color.capitalize()}",
                    unsafe_allow_html=True)

    st.markdown("### Trends (if available)")
    trend_images = {
        "up": "assets/up.png",
        "down": "assets/down.png",
        "no_trend": "assets/no_trend.png",
        "right": "assets/right.png",
        "right-up": "assets/right-up.png"
    }
    for trend, path in trend_images.items():
        if os.path.exists(path):
            st.image(path, width=40, caption=trend.replace("_", " ").capitalize())

# SDG Buttons Section
st.write("---")
st.write("### Explore SDGs")

button_cols = st.columns(8)  # 8 Buttons per row for compact layout

for i, label in enumerate(sdg_labels):
    col = button_cols[i % 8]
    with col:
        # SDG-Bild laden
        image_path = os.path.join('assets', f'{i + 1}.png')
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)

        # Button für SDG
        if st.button(label, key=f"button_{i}"):
            selected_sdg_index = i
            fig = generate_map(selected_sdg_index)
            map_placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

