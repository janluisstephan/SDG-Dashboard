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
if "proceed" not in st.session_state:
    st.session_state.proceed = False
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# Leading question section
if not st.session_state.proceed:
    st.markdown(
        """
        <h1 style="text-align: center; color: #2c3e50; margin-top: 50px;">How reliable are SDG scores in measuring sustainable development progress?</h1>
        <p style="text-align: center; font-size: 16px; color: #7f8c8d;">Please rate on a scale from 1 to 10, where 10 is the most reliable.</p>
        """,
        unsafe_allow_html=True,
    )
    
    # Slider
    reliability_score = st.slider(
        label="Rate the reliability:",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Drag the slider to indicate your opinion on the reliability of SDG scores."
    )

    # Create two columns for Instructions and Bias
    instruction_col, bias_col = st.columns(2)

    with instruction_col:
        st.markdown("## Instructions")
        st.write("""
        1. Select an SDG by clicking the button above its icon below the map.
        2. View the map to see the global performance for the selected SDG.
        3. Use the dropdown under the legend to select a country and view its trend.
        """)

    with bias_col:
        st.markdown("## Bias")
        st.write("""
        The data presented here is aggregated from various global sources and may include uncertainties. 
        Factors such as data quality, collection methods, and regional differences in reporting standards 
        could introduce biases. Interpret trends and performance cautiously, acknowledging these limitations.
        """)

    # Large Proceed button
    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <button style="
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 50px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                margin: 10px auto;
                cursor: pointer;
                border-radius: 5px;
            " onclick="document.location.reload()">Proceed</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Capture button click
    if st.button("Proceed", key="proceed_button"):
        st.session_state.proceed = True
        st.session_state.reliability_score = reliability_score

# Full dashboard
if st.session_state.proceed:
    # Identify SDG and trend columns
    color_columns = [col for col in color_data.columns if col.startswith("SDG")]
    trend_columns = [
        color_data.columns[color_data.columns.get_loc(col) + 1]
        if color_data.columns.get_loc(col) + 1 < len(color_data.columns)
        else None
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
        "➚": "Moderately Increasing",
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
