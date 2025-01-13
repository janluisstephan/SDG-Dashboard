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
        st.markdown("<h2 style='font-size: 24px;'>Introduction</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size: 20px; color: #FF4136;">
        In the context of sustainability we always talk about the Sustainable Development Goals (SDGs). 
        We accept their apparent importance and rarely scrutinize them.
        </p>
        <p style="font-size: 20px; color: #FF4136;">
        Therefore we want to enable you to gain a deeper understanding of the SDGs, how they are constructed, 
        and what their weaknesses are.
        </p>
        """, unsafe_allow_html=True)

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
        st.experimental_rerun()

# SDG dashboard page
if st.session_state.proceed and not st.session_state.new_dashboard:
    if color_data is not None:
        st.title("SDG Dashboard")
        st.write("Welcome to the SDG Dashboard. Explore the data and trends for Sustainable Development Goals.")
    else:
        st.error("SDG data is not available.")

    # Placeholder for more SDG Dashboard content
    if st.button("Proceed to Next Dashboard", key="next_dashboard_button"):
        st.session_state.new_dashboard = True
        st.experimental_rerun()

# Second dashboard
if st.session_state.new_dashboard:
    st.title("Indicator Dashboard")
    st.write("This is the second dashboard where you can explore indicators in more detail.")
