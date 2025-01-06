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

# Funktion für die Karte
def generate_map(selected_sdg_index):
    current_sdg = color_columns[selected_sdg_index]
    filtered_data = color_data["Country"].to_frame()
    filtered_data[current_sdg] = color_data[current_sdg]
    filtered_data.dropna(subset=[current_sdg], inplace=True)
    filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

    fig = px.choropleth(
        filtered_data,
        locations="Country",
        locationmode="country names",
        color="Color",
        hover_name="Country",
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

# Streamlit Layout
st.title("Sustainable Development Goals Dashboard")

# Hauptkarte
col1, col2 = st.columns([4, 1])
with col1:
    st.write("### Global SDG Performance")
    map_placeholder = st.empty()

with col2:
    st.write("### Legend")
    st.write("This section is currently empty.")

# CSS für Buttons mit Hintergrundbildern
button_style = """
<style>
.sdg-button {
    display: inline-block;
    width: 120px;
    height: 120px;
    margin: 10px;
    background-size: cover;
    background-position: center;
    border: none;
    cursor: pointer;
    outline: none;
}
</style>
"""

st.markdown(button_style, unsafe_allow_html=True)

# Buttons mit Bildern und Funktion
st.write("### Explore SDGs")
button_cols = st.columns(4)  # Vier Buttons pro Zeile

# Standardkarte anzeigen: "No Poverty" (Index 0)
selected_sdg_index = 0
fig = generate_map(selected_sdg_index)
map_placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

for i, label in enumerate(sdg_labels):
    col = button_cols[i % 4]
    with col:
        image_path = os.path.join('assets', f'sdg_{i + 1}.png')
        if os.path.exists(image_path):
            st.markdown(
                f"""
                <button class="sdg-button" style="background-image: url('{image_path}');" onclick="window.location.href='/?sdg={i}'">
                </button>
                """,
                unsafe_allow_html=True
            )

        # Karte aktualisieren, wenn ein Button geklickt wird
        query_params = st.experimental_get_query_params()
        if "sdg" in query_params and query_params["sdg"] == [str(i)]:
            selected_sdg_index = i
            fig = generate_map(selected_sdg_index)
            map_placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
