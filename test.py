import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")

# Load data with caching
@st.cache_data
def load_sdg_data():
    data_path = 'Data/SDR2024-data.xlsx'
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')
    return sdg_data, color_data

@st.cache_data
def load_goal7_data():
    data_path = 'Data/goal7.xlsx'
    data = pd.read_excel(data_path, engine='openpyxl')
    return data

# Load SDG and Goal 7 data
sdg_data, color_data = load_sdg_data()
goal7_data = load_goal7_data()

# Initialize session state
if "proceed" not in st.session_state:
    st.session_state.proceed = False
if "selected_sdg_index" not in st.session_state:
    st.session_state.selected_sdg_index = 0
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "new_dashboard" not in st.session_state:
    st.session_state.new_dashboard = False

# SDG Dashboard
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
        st.write("---")
        st.markdown("## Instructions for Dashboard")
        st.write("""
        1. Select an SDG by clicking the button above its icon below the map.
        2. View the map to see the global performance for the selected SDG.
        3. Use the dropdown under the legend to select a country and view its trend.
        """)

    with bias_col:
        st.write("---")
        st.markdown("## Bias")
        st.write("""
        The data presented here is aggregated from various global sources and may include uncertainties. 
        Factors such as data quality, collection methods, and regional differences in reporting standards 
        could introduce biases. Interpret trends and performance cautiously, acknowledging these limitations.
        """)

    # Large Proceed button
    if st.button("Click 2x to proceed to SDG Dashboard", key="proceed_button"):
        st.session_state.proceed = True
        st.session_state.reliability_score = reliability_score

# SDG Dashboard
if st.session_state.proceed and not st.session_state.new_dashboard:
    st.markdown("<h2 style='text-align: center;'>SDG Dashboard</h2>", unsafe_allow_html=True)

    # Add SDG map and buttons here (details omitted for brevity)

    # Button to proceed to the Indicator Dashboard
    if st.button("Click 2x to proceed to Indicator-Dashboard", key="new_dashboard_button"):
        st.session_state.new_dashboard = True

# Indicator Dashboard
if st.session_state.new_dashboard:
    # Filter out rows with missing essential data for Goal 7
    goal7_data = goal7_data.dropna(subset=['Indicator', 'GeoAreaName', 'Value', 'TimePeriod', 'Location'])

    # Initialize session state for selected indicator and countries
    if "selected_indicator" not in st.session_state:
        st.session_state.selected_indicator = "7.1.1"  # Default indicator

    if "selected_countries" not in st.session_state:
        st.session_state.selected_countries = ["Brazil"]  # Default country

    # Sidebar for indicator selection
    st.sidebar.header("Select Indicator")
    indicators = goal7_data["Indicator"].unique()
    st.session_state.selected_indicator = st.sidebar.selectbox(
        "Choose an indicator:",
        options=indicators,
        index=0
    )

    # Sidebar for country selection
    st.sidebar.header("Select Countries")
    countries = goal7_data["GeoAreaName"].unique()
    st.session_state.selected_countries = st.sidebar.multiselect(
        "Choose countries to compare:",
        options=countries,
        default=["Brazil"]  # Default country
    )

    # Filter data based on selected indicator and countries
    filtered_data = goal7_data[
        (goal7_data["Indicator"] == st.session_state.selected_indicator) &
        (goal7_data["GeoAreaName"].isin(st.session_state.selected_countries))
    ]

    # Further split the data into ALLAREA, URBAN, and RURAL
    allarea_data = filtered_data[filtered_data["Location"] == "ALLAREA"]
    urban_data = filtered_data[filtered_data["Location"] == "URBAN"]
    rural_data = filtered_data[filtered_data["Location"] == "RURAL"]

    # Create the interactive graph
    st.title("Indicator Dashboard")
    st.markdown(f"### Indicator: {st.session_state.selected_indicator}")

    if not filtered_data.empty:
        fig = px.line(
            filtered_data,
            x="TimePeriod",
            y="Value",
            color="GeoAreaName",
            line_dash="Location",  # Differentiates ALLAREA, URBAN, and RURAL
            labels={
                "TimePeriod": "Year",
                "Value": "Indicator Value",
                "Location": "Region"
            },
            title="Indicator Trends by Country and Region"
        )
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Indicator Value",
            legend_title="Country / Region",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected indicator and countries.")
