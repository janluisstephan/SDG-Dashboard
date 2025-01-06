import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide")

# Daten laden mit Caching
@st.cache_data
def load_data():
    data_path = 'Data/SDR2024-data.xlsx'
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    return sdg_data

sdg_data = load_data()

# SDG-Spalten identifizieren
color_columns = [col for col in sdg_data.columns if "Dash" in col]
trend_columns = [col for col in sdg_data.columns if "Trend" in col]

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
    filtered_data = sdg_data[["Country", current_sdg]].dropna()
    filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

    fig = px.choropleth(
        filtered_data,
        locations="Country",
        locationmode="country names",
        color="Color",
        hover_name="Country",
        hover_data={"Country": True, "Color": False},
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

# Default selected SDG index
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0

# Default selected country
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# Top row: Instructions, Map, Legend
col1, col2, col3 = st.columns([1.5, 4, 1.5])

# Instructions
with col1:
    st.markdown("## Instructions")
    st.write("""
    1. Select an SDG using the buttons below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Click on a country to view specific trends.
    """)

# Map Placeholder
with col2:
    st.write("### Global SDG Performance")
    fig = generate_map(st.session_state.selected_sdg_index)
    selected_points = plotly_events(fig, click_event=True, override_height=600, override_width="100%")

    # Handle country selection
    if selected_points:
        selected_country = selected_points[0]["hovertext"]
        st.session_state.selected_country = selected_country

# Legend
with col3:
    st.markdown("## Legend")
    st.markdown("### Colors")
    for color, hex_value in color_mapping.items():
        st.markdown(
            f"<div style='background-color: {hex_value}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;'></div> {color.capitalize()}",
            unsafe_allow_html=True)

    if st.session_state.selected_country:
        st.markdown(f"### Trends for {st.session_state.selected_country}")
        trend_images = {
            "↑": "assets/up.png",
            "↓": "assets/down.png",
            "→": "assets/right.png",
            "↗": "assets/right-up.png",
            "-": "assets/no_trend.png"
        }
        # Extract trend for selected country and SDG
        selected_country_data = sdg_data[sdg_data["Country"] == st.session_state.selected_country]
        trend_column = trend_columns[st.session_state.selected_sdg_index]
        if trend_column in selected_country_data.columns and not selected_country_data[trend_column].isna().all():
            trend = selected_country_data.iloc[0][trend_column]
            trend_image = trend_images.get(trend, None)
            if trend_image and os.path.exists(trend_image):
                st.image(trend_image, width=40, caption=f"Trend: {trend}")
        else:
            st.write("No trend data available for this country.")

# SDG Buttons Section
st.write("---")
st.write("### Explore SDGs")

button_cols = st.columns(8)

for i, label in enumerate(sdg_labels):
    col = button_cols[i % 8]
    with col:
        # SDG Image
        image_path = os.path.join('assets', f'{i + 1}.png')
        if os.path.exists(image_path):
            col.image(image_path, use_container_width=True)

        # SDG Button
        if col.button(label, key=f"button_{i}"):
            st.session_state.selected_sdg_index = i
            st.session_state.selected_country = None
            fig = generate_map(st.session_state.selected_sdg_index)
