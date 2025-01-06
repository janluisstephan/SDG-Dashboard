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
    fig = generate_map(st.session_state.selected_sdg_index)
    st.markdown(f"<div class='{blur_class}'>", unsafe_allow_html=True)
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

    st.markdown("<div style='margin-top: 50px;'>", unsafe_allow_html=True)
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
                    <div style='display: flex; align-items: center;' class='{blur_class}'>
                        <span style='font-size: 24px; margin-right: 10px;'>{trend}</span>
                        <span style='font-size: 16px;'>{trend_description}</span>
                    </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SDG selection section
st.write("---")
st.markdown(f"<div class='{blur_class}'>", unsafe_allow_html=True)
cols = st.columns(len(sdg_labels))

for i, col in enumerate(cols):
    with col:
        if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
            st.session_state.selected_sdg_index = i

        image_path = os.path.join("assets", f"{i + 1}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=False, width=130 if i == 6 else 90)  # Highlight SDG 7
st.markdown("</div>", unsafe_allow_html=True)
