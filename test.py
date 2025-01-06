import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import os

st.set_page_config(layout="wide")

# Load data with caching
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
    "Affordable and Clean Energy",  # SDG 7
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
    "green": "Goal Achievement",
    "yellow": "Challenges Remain",
    "orange": "Significant Challenges",
    "red": "Major Challenges",
    "grey": "Insufficient Data"
}

color_hex_mapping = {
    "green": "#2ca02c",
    "yellow": "#ffdd57",
    "orange": "#ffa500",
    "red": "#d62728",
    "grey": "#808080"
}

# Arrow mapping for trends
trend_mapping = {
    "↑": "On track or maintaining achievement",
    "↗": "Moderately Increasing",
    "→": "Stagnating",
    "↓": "Decreasing"
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
        color_discrete_map=color_hex_mapping
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

# Display Trends for Selected Country
def display_country_trend(selected_country, selected_sdg_index):
    if selected_country:
        trend_column = trend_columns[selected_sdg_index]
        trend_data = color_data[color_data["Country"] == selected_country]
        if trend_column in trend_data.columns and not trend_data[trend_column].isna().all():
            trend = trend_data.iloc[0][trend_column]
            trend_description = trend_mapping.get(trend, "Unknown trend")
            st.markdown(f"### Trend for {selected_country}")
            st.markdown(f"""
                <div style='display: flex; align-items: center;'>
                    <span style='font-size: 24px; margin-right: 10px;'>{trend}</span>
                    <span style='font-size: 16px;'>{trend_description}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"### Trend for {selected_country}")
            st.write("No trend data available.")
    else:
        st.write("Click on a country to view its trend.")

# Top row: Instructions, Map, Legend
st.write("---")
header_cols = st.columns([1.5, 4, 1.5])

with header_cols[0]:
    st.markdown("## Instructions")
    st.write("""
    1. Select an SDG by clicking the button above its icon below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Click on a country to view specific trends.
    """)

with header_cols[1]:
    st.markdown("<h2 style='text-align: center; margin-bottom: 10px;'>Global SDG Performance</h2>", unsafe_allow_html=True)
    fig = generate_map(st.session_state.selected_sdg_index)
    selected_points = plotly_events(fig, click_event=True, override_height=600)
    if selected_points:
        country = selected_points[0].get("hovertext")
        if country:
            st.session_state.selected_country = country

with header_cols[2]:
    st.markdown("## Legend")
    for color, description in color_mapping.items():
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='background-color: {color_hex_mapping[color]}; width: 20px; height: 20px; margin-right: 10px;'></div>"
            f"<span style='font-size: 14px;'>{description}</span></div>",
            unsafe_allow_html=True
        )

# Trends Section under Legend
with header_cols[2]:
    display_country_trend(st.session_state.selected_country, st.session_state.selected_sdg_index)

# SDG Icons with Buttons Centered Above
st.write("---")
st.write("### Explore SDGs")

# Create horizontal layout with images and centered buttons
cols = st.columns(len(sdg_labels))  # Create one column per SDG
for i, col in enumerate(cols):
    with col:
        if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
            st.session_state.selected_sdg_index = i
            st.session_state.selected_country = None

        # Display the SDG image
        image_path = os.path.join("assets", f"{i + 1}.png")
        if os.path.exists(image_path):
            if i == 6:  # Highlight SDG 7 (index 6)
                st.image(image_path, use_container_width=False, width=130)  # Larger size for SDG 7
            else:
                st.image(image_path, use_container_width=False, width=90)  # Default size for other SDGs
