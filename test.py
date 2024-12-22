import streamlit as st
import pandas as pd
import plotly.express as px

# Define paths for SDG data
data_path = 'Data/SDR2024-data.xlsx'

# Load data
@st.cache_data
def load_data():
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')
    return sdg_data, color_data

sdg_data, color_data = load_data()

# SDG information
sdg_labels = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education",
    "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy",
    "Decent Work and Economic Growth", "Industry, Innovation and Infrastructure",
    "Reduced Inequalities", "Sustainable Cities and Communities",
    "Responsible Consumption and Production", "Climate Action", "Life Below Water",
    "Life on Land", "Peace, Justice and Strong Institutions", "Partnerships for the Goals"
]

# Cache the map figures
@st.cache_data
def prepare_all_figures():
    all_figures = {}
    for idx, sdg in enumerate(sdg_labels):
        column_name = f"SDG{idx + 1}: {sdg}"
        if column_name in color_data.columns:
            filtered_data = color_data[["Country", column_name]].dropna()
            filtered_data.columns = ["Country", "Color"]
            fig = px.choropleth(
                filtered_data,
                locations="Country",
                locationmode="country names",
                color="Color",
                title=sdg
            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            all_figures[sdg] = fig
    return all_figures

all_figures = prepare_all_figures()

# Streamlit app setup
st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")
st.title("🌍 Sustainable Development Goals Dashboard")

# Dropdown menu for SDG selection
selected_sdg = st.selectbox("Select an SDG:", sdg_labels)

# Display the selected SDG
st.header(f"Selected SDG: {selected_sdg}")
st.plotly_chart(all_figures[selected_sdg], use_container_width=True)
