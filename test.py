import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json  # Importiere das json-Modul

st.set_page_config(layout="wide")

# Speicherort der Antworten
DATA_FILE = "lib.py"

# Funktion zum Laden der Antworten
def load_answers():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Leere Liste, falls die Datei leer oder ungültig ist
    else:
        return []  # Leere Liste, wenn die Datei nicht existiert

# Funktion zum Speichern der Antworten
def save_answer(reliability, knowledge):
    answers = load_answers()
    answers.append({"reliability_score": reliability, "sdg_knowledge_score": knowledge})
    with open(DATA_FILE, "w") as file:
        json.dump(answers, file, indent=4)

# Lade gespeicherte Daten, falls vorhanden
answers = load_answers()

# Funktion zum Laden der SDG-Daten
@st.cache_data
def load_data():
    data_path = "Data/SDR2024-data.xlsx"
    if os.path.exists(data_path):
        sdg_data = pd.read_excel(data_path, sheet_name="Full Database", engine="openpyxl")
        color_data = pd.read_excel(data_path, sheet_name="Overview", engine="openpyxl")
        return sdg_data, color_data
    else:
        st.error("Data file not found! Make sure 'SDR2024-data.xlsx' is in the 'Data' directory.")
        return None, None

# Lade SDG-Daten
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
if "results_shown" not in st.session_state:
    st.session_state.results_shown = False
if "last_page" not in st.session_state:
    st.session_state.last_page = None

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
        <h1 style="text-align: center; color: #2c3e50; margin-top: 30px;">How would you rate your knowledge about the composition of SDGs?</h1>
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

    # Two columns: Guideline on the left, Bias on the right
    guideline_col, bias_col = st.columns(2)

    with guideline_col:
        st.write("---")
        st.markdown("## Introduction")
        st.write("""
        In the context of sustainability we always talk about the Sustainable Development Goals (SDGs). 
        We accept their apparent importance and rarely scrutinize them. 

        Therefore we want to enable you to gain a deeper understanding of the SDGs, how they are constructed, 
        and what their weaknesses are.
        """)

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

    # Large Proceed button
    if st.button("Click 2x to proceed to SDG Dashboard", key="proceed_button"):
        # Save the answers
        save_answer(reliability_score, sdg_knowledge_score)
        st.session_state.proceed = True
        st.session_state.reliability_score = reliability_score
        st.session_state.sdg_knowledge_score = sdg_knowledge_score

# SDG dashboard
if st.session_state.proceed and not st.session_state.new_dashboard:
    if color_data is not None:
        # Identify SDG and trend columns
        color_columns = [col for col in color_data.columns if col.startswith("SDG")]
        trend_columns = [
            color_data.columns[color_data.columns.get_loc(col) + 1]
            if color_data.columns.get_loc(col) + 1 < len(color_data.columns)
            else None
            for col in color_columns
        ]
        st.write("SDG Dashboard Placeholder")
    else:
        st.error("SDG data is not available.")

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
            dragmode=False,
            annotations=[
                dict(
                    x=0.94,  # Adjust x-coordinate for placement (right bottom)
                    y=0.001,  # Adjust y-coordinate for placement (bottom)
                    xref="paper",
                    yref="paper",
                    text="Status: 2024",  # The note text
                    showarrow=False,
                    font=dict(size=12, color="black"),
                    align="right"
                )
            ]
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
        
        # Add the Tip for the user
        st.markdown("## Tip")
        st.write("""
        Have a look at Brazil's performance at the SDG 7. Did you expect that?
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

# Check if the results page should be displayed
if "results_shown" in st.session_state and st.session_state.results_shown:
    # RESULTS PAGE
    st.title("Results")
    st.markdown("### Here are the responses you've provided:")
    for idx, answer in enumerate(answers):
        st.write(f"**Response {idx + 1}:**")
        st.write(f"- Reliability Score: {answer['reliability_score']}")
        st.write(f"- SDG Knowledge Score: {answer['sdg_knowledge_score']}")

    # Add a button to return to the main dashboard
    if st.button("Click 2x to return to Dashboard"):
        st.session_state.results_shown = False
        st.session_state.new_dashboard = True
        st.experimental_rerun()

elif st.session_state.new_dashboard:
    # INDICATOR DASHBOARD
    st.sidebar.header("Dashboard Selection")
    dashboard_choice = st.sidebar.radio(
        "Choose a dashboard:",
        options=["Indicator Dashboard", "Electricity Loss Comparison"],
        index=0
    )

    if dashboard_choice == "Indicator Dashboard":
        @st.cache_data
        def load_goal7_data():
            data_path = 'Data/Goal7.xlsx'
            data = pd.read_excel(data_path, engine='openpyxl')
            return data

        goal7_data = load_goal7_data()
        goal7_data["Indicator"] = goal7_data["Indicator"].str.strip()
        goal7_data = goal7_data.dropna(subset=['Indicator', 'GeoAreaName', 'Value', 'TimePeriod'])

        # Sidebar for selecting indicators and countries
        st.sidebar.header("Select Indicator and Countries")
        indicators = sorted(goal7_data["Indicator"].unique())
        selected_indicator = st.sidebar.selectbox("Choose an indicator:", options=indicators)
        countries = sorted(goal7_data["GeoAreaName"].unique())
        selected_countries = st.sidebar.multiselect("Choose countries to compare:", options=countries, default=["Brazil", "Germany"])

        if st.sidebar.button("Generate Indicator Graph"):
            filtered_data = goal7_data[
                (goal7_data["Indicator"] == selected_indicator) &
                (goal7_data["GeoAreaName"].isin(selected_countries))
            ]

            st.title("Indicator Dashboard")
            if not filtered_data.empty:
                if selected_indicator == "7.1.1":
                    st.markdown("### Indicator 7.1.1: Proportion of population with access to electricity, by urban/rural (%). Electrification data are collected from industry, national surveys and international sources")
                    filtered_data["Value"] = filtered_data["Value"].interpolate(method="linear")

                    fig = px.line(
                        filtered_data,
                        x="TimePeriod",
                        y="Value",
                        color="GeoAreaName",
                        line_dash="Location",
                        labels={"TimePeriod": "Year", "Value": "Access Percentage"},
                        title="Access to Electricity (by Location and Country)",
                        markers=True
                    )
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif selected_indicator == "7.1.2":
                    st.markdown("### Indicator 7.1.2: Proportion of population with primary reliance on clean fuels and technology (%). This is calculated as the number of people using clean fuels and technologies for cooking, heating and lighting divided by total population reporting that any cooking, heating or lighting, expressed as percentage. “Clean” is defined by the emission rate targets and specific fuel recommendations (i.e. against unprocessed coal and kerosene) included in the normative guidance WHO guidelines for indoor air quality: household fuel combustion.")
                    filtered_data["Value"] = filtered_data["Value"].interpolate(method="linear")

                    # Handle error bounds gracefully without warning
                    error_y = None
                    error_y_minus = None
                    if "UpperBou" in filtered_data.columns and "LowerBou" in filtered_data.columns:
                        error_y = filtered_data["UpperBou"] - filtered_data["Value"]
                        error_y_minus = filtered_data["Value"] - filtered_data["LowerBou"]

                    fig = px.line(
                        filtered_data,
                        x="TimePeriod",
                        y="Value",
                        color="GeoAreaName",
                        line_dash="Location",
                        error_y=error_y,
                        error_y_minus=error_y_minus,
                        labels={"TimePeriod": "Year", "Value": "Reliance Percentage"},
                        title="Reliance on Clean Fuels (by Location and Country)",
                        markers=True
                    )
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif selected_indicator == "7.2.1":
                    st.markdown("### Indicator 7.2.1: Renewable energy share in the total final energy consumption (%)")
                    filtered_data["Value"] = filtered_data["Value"].interpolate(method="linear")

                    fig = px.line(
                        filtered_data,
                        x="TimePeriod",
                        y="Value",
                        color="GeoAreaName",
                        title="Renewable Energy Share",
                        labels={"TimePeriod": "Year", "Value": "Renewable Energy Share (%)"},
                        markers=True
                    )
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif selected_indicator == "7.3.1":
                    st.markdown("### Indicator 7.3.1: Energy intensity level of primary energy (megajoules per constant 2017 purchasing power parity GDP)")
                    fig = px.line(
                        filtered_data,
                        x="TimePeriod",
                        y="Value",
                        color="GeoAreaName",
                        title="Energy Intensity Level (Primary Energy)",
                        labels={"TimePeriod": "Year", "Value": "Energy Intensity"},
                        markers=True
                    )
                    fig.update_layout(template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif selected_indicator == "7.a.1" or selected_indicator == "7.b.1":
                    st.markdown(f"### Indicator {selected_indicator}: Financial flows and renewable energy production")
                    if "Type of renewable technology" in filtered_data.columns:
                        for technology in filtered_data["Type of renewable technology"].unique():
                            tech_data = filtered_data[filtered_data["Type of renewable technology"] == technology]
                            tech_data = tech_data.sort_values("TimePeriod").reset_index(drop=True)

                            fig = px.bar(
                                tech_data,
                                x="TimePeriod",
                                y="Value",
                                color="GeoAreaName",
                                barmode="group",
                                title=f"{technology} Trends ({selected_indicator})",
                                labels={"TimePeriod": "Year", "Value": "Value (in Units)"}
                            )
                            fig.update_layout(template="plotly_white")
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("The column 'Type of renewable technology' is missing in the data.")

            else:
                st.write("No data available for the selected indicator and countries.")



        # Button to proceed to results
        st.sidebar.write("---")
        if st.sidebar.button("Click 2x to proceed", key="proceed_to_results_button"):
            st.session_state.results_shown = True  # Switch to results page
            st.experimental_rerun()

    elif dashboard_choice == "Electricity Loss Comparison":
        @st.cache_data
        def load_elecloss2_data():
            data_path = 'Data/elecloss2.csv'
            data = pd.read_csv(data_path, skiprows=4)
            return data

        elecloss2_data = load_elecloss2_data()
        st.sidebar.header("Select Countries for Electricity Loss")
        countries = sorted(elecloss2_data["Country Name"].dropna().unique())
        selected_countries = st.sidebar.multiselect(
            "Choose up to two countries to compare:",
            options=countries,
            default=["Brazil", "Germany"]
        )

        if st.sidebar.button("Generate Comparison"):
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
                labels={"Year": "Year", "Electricity Loss (%)": "Electricity Loss (%)", "Country Name": "Country"},
                title="Electric Power Transmission and Distribution Loss Comparison"
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        elif not selected_countries:
            st.warning("Please select at least one country for the comparison.")

        # Button to proceed to results
        st.sidebar.write("---")
        if st.sidebar.button("Click 2x to proceed", key="proceed_to_results_button"):
            st.session_state.results_shown = True  # Switch to results page
            st.experimental_rerun()

    elif dashboard_choice == "Electricity Loss Comparison":
        @st.cache_data
        def load_elecloss2_data():
            data_path = 'Data/elecloss2.csv'
            data = pd.read_csv(data_path, skiprows=4)
            return data

        elecloss2_data = load_elecloss2_data()
        st.sidebar.header("Select Countries for Electricity Loss")
        countries = sorted(elecloss2_data["Country Name"].dropna().unique())
        selected_countries = st.sidebar.multiselect(
            "Choose up to two countries to compare:",
            options=countries,
            default=["Brazil", "Germany"]
        )

        if st.sidebar.button("Generate Comparison"):
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
                labels={"Year": "Year", "Electricity Loss (%)": "Electricity Loss (%)", "Country Name": "Country"},
                title="Electric Power Transmission and Distribution Loss Comparison"
            )
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        elif not selected_countries:
            st.warning("Please select at least one country for the comparison.")


        # Button to proceed to results
        st.sidebar.write("---")
        if st.sidebar.button("Click 2x to proceed", key="proceed_to_results_button"):
            st.session_state.results_shown = True  # Switch to results page
            st.experimental_rerun()

    elif dashboard_choice == "Electricity Loss Comparison":
        @st.cache_data
        def load_elecloss2_data():
            data_path = 'Data/elecloss2.csv'
            data = pd.read_csv(data_path, skiprows=4)
            return data

        elecloss2_data = load_elecloss2_data()
        st.sidebar.header("Select Countries for Electricity Loss")
        countries = sorted(elecloss2_data["Country Name"].dropna().unique())
        selected_countries = st.sidebar.multiselect(
            "Choose several countries to compare:",
            options=countries,
            default=["Brazil", "Germany", "World"]
        )

        if st.sidebar.button("Generate Comparison"):
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
                labels={"Year": "Year", "Electricity Loss (%)": "Electricity Loss (%)", "Country Name": "Country"},
                title="Electric Power Transmission and Distribution Loss Comparison"
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Electricity Loss (%)",
                legend_title="Country",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif not selected_countries:
            st.warning("Please select at least one country for the comparison.")
