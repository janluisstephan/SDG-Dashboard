import streamlit as st
import pandas as pd
import plotly.express as px
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

# Identify SDG and trend columns
color_columns = [col for col in color_data.columns if col.startswith("SDG")]
trend_columns = [
    color_data.columns[color_data.columns.get_loc(col) + 1] if color_data.columns.get_loc(col) + 1 < len(color_data.columns) else None
    for col in color_columns
]

# SDG labels
sdg_labels = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education",
    "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy",
    "Decent Work and Economic Growth", "Industry, Innovation and Infrastructure",
    "Reduced Inequalities", "Sustainable Cities and Communities",
    "Responsible Consumption and Production", "Climate Action", "Life Below Water",
    "Life on Land", "Peace, Justice and Strong Institutions", "Partnerships for the Goals"
]

# Color and trend mappings
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
trend_mapping = {
    "↑": "On track or maintaining achievement",
    "↗": "Moderately Increasing",
    "→": "Stagnating",
    "↓": "Decreasing"
}

# Generate map
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

# Default session states
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# Layout: Instructions, Map, Legend
st.write("---")
header_cols = st.columns([1.5, 4, 1.5])

with header_cols[0]:
    st.markdown("## Instructions")
    st.write("""
    1. Select an SDG by clicking the button above its icon below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Use the dropdown under the legend to select a country and view its trend.
    
    """)
    st.markdown("## Bias")
    st.write("""
    The data presented here is aggregated from various global sources and may include uncertainties. Factors such as data quality, 
    collection methods, and regional differences in reporting standards could introduce biases. Interpret trends and performance 
    cautiously, acknowledging these limitations.
    """)

with header_cols[1]:
    st.markdown("<h2 style='text-align: center; margin-bottom: 10px;'>Global SDG Performance</h2>", unsafe_allow_html=True)
    fig = generate_map(st.session_state.selected_sdg_index)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with header_cols[2]:
    st.markdown("## Legend")
    for color, description in color_mapping.items():
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='background-color: {color_hex_mapping[color]}; width: 20px; height: 20px; margin-right: 10px;'></div>"
            f"<span style='font-size: 14px;'>{description}</span></div>",
            unsafe_allow_html=True
        )

    # Add country selection dropdown and trend display
    st.markdown("### Trend for")
    selected_country = st.selectbox("Select a country:", options=color_data["Country"].unique(), key="country_dropdown")

    if selected_country:
        trend_column = trend_columns[st.session_state.selected_sdg_index]
        if trend_column and trend_column in color_data.columns:
            trend_data = color_data[color_data["Country"] == selected_country]
            if not trend_data.empty and trend_column in trend_data.columns:
                trend = trend_data.iloc[0][trend_column]
                trend_description = trend_mapping.get(str(trend).strip(), "No trend description available.")
                st.markdown(f"""
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 24px; margin-right: 10px;'>{trend}</span>
                        <span style='font-size: 16px;'>{trend_description}</span>
                    </div>
                """, unsafe_allow_html=True)

# SDG selection section
st.write("---")
st.write("### Explore SDGs")

cols = st.columns(len(sdg_labels))

for i, col in enumerate(cols):
    with col:
        if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
            st.session_state.selected_sdg_index = i

        image_path = os.path.join("assets", f"{i + 1}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=False, width=130 if i == 6 else 90)  # Highlight SDG 7
