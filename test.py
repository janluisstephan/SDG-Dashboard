import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load the data
@st.cache_data
def load_data():
    data_path = 'Data/SDR2024-data.xlsx'
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')
    return sdg_data, color_data

sdg_data, color_data = load_data()

# Define SDG columns
sdg_columns = [col for col in sdg_data.columns if "Goal" in col and "Score" in col]
color_columns = [col for col in color_data.columns if col.startswith("SDG")]

# Define trend columns
trend_columns = [
    color_data.columns[color_data.columns.get_loc(col) + 1] if color_data.columns.get_loc(col) + 1 < len(color_data.columns) else None
    for col in color_columns
]

# SDG Labels
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

# Color mapping
color_mapping = {
    "green": "#2ca02c",
    "yellow": "#ffdd57",
    "orange": "#ffa500",
    "red": "#d62728",
    "grey": "#808080"
}

# Streamlit Layout
st.title("Sustainable Development Goals Dashboard")

# Add Instructions Section
st.markdown("## Instructions")
st.write("""
1. Select a Sustainable Development Goal (SDG) from the buttons below.
2. View the map showing the performance of countries for the selected SDG.
3. Check the legend to understand the color coding.
""")

# Dropdown for SDG selection (hidden for now, replaced by buttons later)
selected_sdg_label = st.selectbox("Choose an SDG:", sdg_labels)
selected_sdg_index = sdg_labels.index(selected_sdg_label)
current_sdg = color_columns[selected_sdg_index]
current_trend = trend_columns[selected_sdg_index]

# Prepare data for the map
filtered_data = color_data[["Country", current_sdg]].dropna()
filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

# Create Map
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
    margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Remove white margins
    paper_bgcolor="#f9f9f9",
    plot_bgcolor="#f9f9f9",
    showlegend=False,
    dragmode=False  # Static map
)

# Layout with three sections: Instructions, Map + Legend, Buttons
st.write("---")

col1, col2 = st.columns([4, 1])  # 80% for map, 20% for legend

with col1:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("## Legend")
    for color, hex_value in color_mapping.items():
        st.markdown(f"<div style='background-color: {hex_value}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;'></div> {color.capitalize()}",
                    unsafe_allow_html=True)

st.write("---")

# Add SDG Buttons with Images
st.markdown("### Select an SDG")

button_cols = st.columns(9)  # Divide buttons into two rows of 9 columns each
sdg_image_base_url = "https://github.com/your-repo/assets"  # Replace with your GitHub repo link

for i, label in enumerate(sdg_labels):
    image_url = f"{sdg_image_base_url}/SDG{i + 1}.png"
    if button_cols[i % 9].button(f"{label}", key=f"button_{i}"):
        selected_sdg_label = label
        selected_sdg_index = i
        current_sdg = color_columns[selected_sdg_index]
        current_trend = trend_columns[selected_sdg_index]
        # Update map data and redraw
        filtered_data = color_data[["Country", current_sdg]].dropna()
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
        col1.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

