import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")

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
    1. Select an SDG by clicking the button above its icon below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Click on a country to view specific trends.
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
        st.markdown(
            f"<div style='background-color: {hex_value}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;'></div> {color.capitalize()}",
            unsafe_allow_html=True)

    if st.session_state.selected_country:
        st.markdown(f"### Trends for {st.session_state.selected_country}")
        trend_images = {
            "up": "assets/up.png",
            "down": "assets/down.png",
            "no_trend": "assets/no_trend.png",
            "right": "assets/right.png",
            "right-up": "assets/right-up.png"
        }
        trend_data = color_data[color_data["Country"] == st.session_state.selected_country]
        trend_column = trend_columns[st.session_state.selected_sdg_index]
        if trend_column in trend_data.columns and not trend_data[trend_column].isna().all():
            trend = trend_data.iloc[0][trend_column]
            trend_image = trend_images.get(trend, None)
            if trend_image and os.path.exists(trend_image):
                st.image(trend_image, width=40, caption=f"Trend: {trend.capitalize()}")
        else:
            st.write("No trend data available for this country.")

# SDG Icons with Buttons Centered Above
st.write("---")
st.write("### Explore SDGs")

# Create horizontal layout with images and centered buttons
cols = st.columns(len(sdg_labels))  # Create one column per SDG
for i, col in enumerate(cols):
    with col:
        # Button above the image
        if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
            st.session_state.selected_sdg_index = i
            st.session_state.selected_country = None
        # Display the SDG image
        image_path = os.path.join('assets', f'{i + 1}.png')
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)

# Generate Map
fig = generate_map(st.session_state.selected_sdg_index)
map_placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
