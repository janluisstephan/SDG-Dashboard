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

# Initialize session state
if "understood" not in st.session_state:
    st.session_state.understood = False
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0  # Default SDG index

# CSS for blurring effect
blurry_style = """
<style>
.blurry {
    filter: blur(8px);
    pointer-events: none;
    opacity: 0.5;
}
</style>
"""

# Generate map
def generate_map(selected_sdg_index):
    try:
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
    except Exception as e:
        st.error(f"Error generating map: {e}")
        return None

# Color and trend mappings
color_columns = [col for col in color_data.columns if col.startswith("SDG")]
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

# Instructions and Bias section
st.write("---")
header_cols = st.columns([1.5, 4, 1.5])

with header_cols[0]:
    st.markdown("## Instructions")
    st.write("""
    1. Select an SDG by clicking the button above its icon below the map.
    2. View the map to see the global performance for the selected SDG.
    3. Use the dropdown under the legend to select a country and view its trend.
    
    ### Bias
    The data presented here is aggregated from various global sources and may include uncertainties. Factors such as data quality, collection methods, and regional differences in reporting standards could introduce biases. Interpret trends and performance cautiously, acknowledging these limitations.
    """)

    # Add "Understood" button
    if not st.session_state.understood:
        if st.button("Understood"):
            st.session_state.understood = True

# Apply blurry style if user has not clicked "Understood"
if not st.session_state.understood:
    st.markdown(blurry_style, unsafe_allow_html=True)
    blur_class = "blurry"
else:
    blur_class = ""

# Conditional rendering of the rest of the dashboard
with header_cols[1]:
    st.markdown("<h2 style='text-align: center; margin-bottom: 10px;'>Global SDG Performance</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='{blur_class}'>", unsafe_allow_html=True)
    fig = generate_map(st.session_state.selected_sdg_index)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with header_cols[2]:
    st.markdown("## Legend")
    st.markdown(f"<div class='{blur_class}'>", unsafe_allow_html=True)
    for color, description in color_mapping.items():
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='background-color: {color_hex_mapping[color]}; width: 20px; height: 20px; margin-right: 10px;'></div>"
            f"<span style='font-size: 14px;'>{description}</span></div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

# SDG selection section
st.write("---")
st.markdown(f"<div class='{blur_class}'>", unsafe_allow_html=True)
cols = st.columns(len(color_columns))

for i, col in enumerate(cols):
    with col:
        if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
            st.session_state.selected_sdg_index = i

        image_path = os.path.join("assets", f"{i + 1}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=False, width=130 if i == 6 else 90)  # Highlight SDG 7
st.markdown("</div>", unsafe_allow_html=True)
