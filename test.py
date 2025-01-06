import streamlit as st
import pandas as pd
import plotly.express as px

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

# Trend image mapping
trend_image_mapping = {
    "up": "assets/up.png",
    "down": "assets/down.png",
    "no_trend": "assets/no_trend.png",
    "right": "assets/right.png",
    "right-up": "assets/right-up.png"
}

# Streamlit Layout
st.title("Sustainable Development Goals Dashboard")

# Add Instructions Section
st.markdown("## Instructions")
st.write("""
1. Select a Sustainable Development Goal (SDG) from the buttons below.
2. View the map showing the performance of countries for the selected SDG.
3. Check the legend to understand the color coding and trends.
""")

# Default selected SDG (initial load)
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0

# Retrieve the current SDG
current_sdg_index = st.session_state.selected_sdg_index
current_sdg = color_columns[current_sdg_index]
current_trend = trend_columns[current_sdg_index]

# Prepare data for the map
filtered_data = color_data[["Country", current_sdg]].dropna()
filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

# Create the map
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

# Layout with two sections: Map + Legend and SDG Buttons
col1, col2 = st.columns([4, 1])  # 80% for map, 20% for legend

with col1:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("## Legend")
    # Color coding legend
    st.markdown("### Colors")
    for color, hex_value in color_mapping.items():
        st.markdown(f"<div style='background-color: {hex_value}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;'></div> {color.capitalize()}",
                    unsafe_allow_html=True)

    # Trend legend
    st.markdown("### Trends")
    for trend_name, image_path in trend_image_mapping.items():
        st.image(image_path, width=30, caption=trend_name.replace("_", " ").capitalize())

st.write("---")

# Add SDG Buttons with Images
st.markdown("### Select an SDG")

button_cols = st.columns(9)  # Divide buttons into two rows of 9 columns each
sdg_image_base_url = "https://github.com/your-repo/assets"  # Replace with your GitHub repo link

for i, label in enumerate(sdg_labels):
    col = button_cols[i % 9]
    image_url = f"{sdg_image_base_url}/{i + 1}.png"  # Update to your actual image URL
    col.image(image_url, use_column_width=True)  # Display the SDG icon
    if col.button(label, key=f"button_{i}"):
        st.session_state.selected_sdg_index = i
        st.experimental_rerun()
