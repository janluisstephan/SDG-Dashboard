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
if "new_dashboard" not in st.session_state:
    st.session_state.new_dashboard = False

# Leading question section
if not st.session_state.proceed:
    st.markdown(
        """
        <h1 style="text-align: center; color: #2c3e50; margin-top: 50px;">How reliable are SDG scores in measuring sustainable development progress?</h1>
        <p style="text-align: center; font-size: 16px; color: #7f8c8d;">Please rate on a scale from 1 to 10, where 10 is the most reliable.</p>
        """,
        unsafe_allow_html=True,
    )

    # Slider for reliability score
    reliability_score = st.slider(
        label="Rate the reliability:",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Drag the slider to indicate your opinion on the reliability of SDG scores."
    )

    # Second question with slider
    st.markdown(
        """
        <h1 style="text-align: center; color: #2c3e50; margin-top: 30px;">How would you rate your knowledge about the concept of SDGs?</h1>
        <p style="text-align: center; font-size: 16px; color: #7f8c8d;">Please rate on a scale from 1 to 10, where 10 means you have excellent knowledge.</p>
        """,
        unsafe_allow_html=True,
    )

    # Slider for SDG knowledge
    sdg_knowledge_score = st.slider(
        label="Rate your knowledge:",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="Drag the slider to indicate your knowledge about the concept of SDGs."
    )

    # Two columns: Bias on the left, Guideline on the right
    bias_col, guideline_col = st.columns(2)

    with bias_col:
        st.write("---")
        st.markdown("## Bias")
        with st.expander("Read more about Bias..."):
            st.write("""
            The data presented here is aggregated from various global sources and may include uncertainties. 
            Factors such as data quality, collection methods, and regional differences in reporting standards 
            could introduce biases. Interpret trends and performance cautiously, acknowledging these limitations.

            The data we introduce may construct a narrative. As we cannot include all existing data in the current version, 
            we decided to provide the data that creates contrast and serves the investigation of our leading question. 
            This is undeterrable and induced by selective bias.
            """)

    with guideline_col:
        st.write("---")
        st.markdown("## Guideline for the Dashboard")
        st.write("""
        In the context of sustainability we always talk about the Sustainable Development Goals (SDGs). 
        We accept their apparent importance and rarely scrutinize them. 

        Therefore we want to enable you to gain a deeper understanding of the SDGs, how they are constructed, 
        and what their weaknesses are.
        """)

    # Large Proceed button
    if st.button("Click 2x to proceed to SDG Dashboard", key="proceed_button"):
        st.session_state.proceed = True
        st.session_state.reliability_score = reliability_score
        st.session_state.sdg_knowledge_score = sdg_knowledge_score


# SDG dashboard
if st.session_state.proceed and not st.session_state.new_dashboard:
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
    header_cols = st.columns([1.5, 4, 1.5])

    with header_cols[0]:
        st.markdown("## Instructions")
        st.write("""
        1. Select an SDG by clicking the button above its icon below the map.
        2. View the map to see the global performance for the selected SDG.
        3. Use the dropdown under the legend to select a country and view its trend.
        """)

        st.markdown("## Bias")
        with st.expander("Read more about Bias..."):
            st.write("""
            The data presented here is aggregated from various global sources and may include uncertainties. 
            Factors such as data quality, collection methods, and regional differences in reporting standards 
            could introduce biases. Interpret trends and performance cautiously, acknowledging these limitations.

            The data we introduce may construct a narrative. As we cannot include all existing data in the current version, 
            we decided to provide the data that creates contrast and serves the investigation of our leading question. 
            This is undeterrable and induced by selective bias.
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

        # Add country selection dropdown and current situation display
        st.markdown("<div style='margin-top: 50px;'>", unsafe_allow_html=True)
        selected_sdg_label = sdg_labels[st.session_state.selected_sdg_index]
        st.markdown(f"### Trend for {selected_sdg_label}")

        selected_country = st.selectbox("Select a country:", options=color_data["Country"].unique(), key="country_dropdown")

        if selected_country:
            current_sdg = color_columns[st.session_state.selected_sdg_index]
            if current_sdg in color_data.columns:
                country_data = color_data[color_data["Country"] == selected_country]
                if not country_data.empty:
                    country_color = country_data.iloc[0][current_sdg]
                    color_description = color_mapping.get(country_color, "No description available.")
                    color_hex = color_hex_mapping.get(country_color, "#808080")
                    st.markdown(f"""
                        <div style='display: flex; align-items: center; margin-top: 10px;'>
                            <div style='background-color: {color_hex}; width: 20px; height: 20px; margin-right: 10px;'></div>
                            <span style='font-size: 16px;'>{color_description}</span>
                        </div>
                    """, unsafe_allow_html=True)

            # Fetch and display trend
            trend_column = trend_columns[st.session_state.selected_sdg_index]
            if trend_column in color_data.columns:
                trend_data = color_data[color_data["Country"] == selected_country]
                if not trend_data.empty:
                    trend = trend_data.iloc[0][trend_column]
                    trend_description = trend_mapping.get(str(trend).strip(), "No trend description available.")
                    st.markdown(f"""
                        <div style='display: flex; align-items: center;'>
                            <span style='font-size: 24px; margin-right: 10px;'>{trend}</span>
                            <span style='font-size: 16px;'>{trend_description}</span>
                        </div>
                    """, unsafe_allow_html=True)

        # Add Proceed button under the Trend display
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        if st.button("Click 2x to proceed to Indicator-Dashboard", key="new_dashboard_button"):
            st.session_state.new_dashboard = True

    # SDG selection section
    st.write("---")
    cols = st.columns(len(sdg_labels))

    for i, col in enumerate(cols):
        with col:
            if st.button(f"SDG {i + 1}", key=f"sdg_button_{i}"):
                st.session_state.selected_sdg_index = i

            image_path = os.path.join("assets", f"{i + 1}.png")
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=False, width=130 if i == 6 else 90)

# Indicator Dashboard
# Indicator Dashboard
if st.session_state.new_dashboard:
    # Tabs for switching between Indicator Dashboard and Electricity Loss Comparison
    tab1, tab2 = st.tabs(["Indicator Dashboard", "Electricity Loss Comparison"])

    # Tab 1: Original Indicator Dashboard
    with tab1:
        # Load the Goal 7 data only once
        @st.cache_data
        def load_goal7_data():
            data_path = 'Data/Goal7.xlsx'
            data = pd.read_excel(data_path, engine='openpyxl')
            return data

        goal7_data = load_goal7_data()

        # Preprocess the dataset
        goal7_data["Indicator"] = goal7_data["Indicator"].str.strip()  # Remove leading/trailing spaces
        goal7_data = goal7_data.dropna(subset=['Indicator', 'GeoAreaName', 'Value', 'TimePeriod'])  # Handle missing values

        # Sidebar for indicator and country selection
        st.sidebar.header("Select Indicator")
        indicators = sorted(goal7_data["Indicator"].unique())
        selected_indicator = st.sidebar.selectbox("Choose an indicator:", options=indicators)

        st.sidebar.header("Select Countries")
        countries = sorted(goal7_data["GeoAreaName"].unique())
        selected_countries = st.sidebar.multiselect("Choose countries to compare:", options=countries, default=["Brazil"])

        generate_indicator_graph = st.sidebar.button("Generate Indicator Graph")

        if generate_indicator_graph:
            # Filter data for the selected indicator and countries
            filtered_data = goal7_data[
                (goal7_data["Indicator"] == selected_indicator) &
                (goal7_data["GeoAreaName"].isin(selected_countries))
            ]

            st.title("Indicator Dashboard")
            st.markdown(f"### Indicator: {selected_indicator}")

            if not filtered_data.empty:
                fig = px.line(
                    filtered_data,
                    x="TimePeriod",
                    y="Value",
                    color="GeoAreaName",
                    labels={
                        "TimePeriod": "Year",
                        "Value": "Indicator Value",
                        "GeoAreaName": "Country"
                    },
                    title=f"Trends for {selected_indicator}",
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Indicator Value",
                    legend_title="Country",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No data available for the selected indicator and countries.")

    # Tab 2: Electricity Loss Comparison
    with tab2:
        # Load the elecloss2.csv dataset
        @st.cache_data
        def load_elecloss2_data():
            data_path = 'Data/elecloss2.csv'
            data = pd.read_csv(data_path, skiprows=4)
            return data

        elecloss2_data = load_elecloss2_data()

        st.sidebar.header("Electricity Loss Comparison")
        countries = sorted(elecloss2_data["Country Name"].dropna().unique())
        selected_countries = st.sidebar.multiselect("Choose two countries to compare:", options=countries, default=countries[:2])

        generate_comparison = st.sidebar.button("Generate Comparison")

        if generate_comparison and len(selected_countries) == 2:
            filtered_data = elecloss2_data[elecloss2_data["Country Name"].isin(selected_countries)]

            melted_data = filtered_data.melt(
                id_vars=["Country Name"], 
                var_name="Year", 
                value_name="Electricity Loss (%)"
            )

            melted_data = melted_data[melted_data["Year"].str.isdigit()]
            melted_data["Year"] = melted_data["Year"].astype(int)

            fig = px.line(
                melted_data,
                x="Year",
                y="Electricity Loss (%)",
                color="Country Name",
                labels={
                    "Year": "Year",
                    "Electricity Loss (%)": "Electricity Loss (%)",
                    "Country Name": "Country"
                },
                title="Electric Power Transmission and Distribution Loss Comparison"
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Electricity Loss (%)",
                legend_title="Country",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        elif len(selected_countries) != 2:
            st.warning("Please select exactly two countries for comparison.")
