import streamlit as st
import pandas as pd
import plotly.express as px

# Define paths for SDG images and data
sdg_images_path = 'assets/'
data_path = 'Data/SDR2024-data.xlsx'

# Load data
def load_data():
    sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
    color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')
    color_data.columns = color_data.columns.str.strip()  # Remove unwanted spaces in column names
    return sdg_data, color_data

sdg_data, color_data = load_data()

# Debugging: Output the columns in color_data
st.write("Spalten in 'color_data':", color_data.columns.tolist())

# SDG information
sdg_labels = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education",
    "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy",
    "Decent Work and Economic Growth", "Industry, Innovation and Infrastructure",
    "Reduced Inequalities", "Sustainable Cities and Communities",
    "Responsible Consumption and Production", "Climate Action", "Life Below Water",
    "Life on Land", "Peace, Justice and Strong Institutions", "Partnerships for the Goals"
]

# Map image paths to SDGs
sdg_images = [f"{sdg_images_path}{i + 1}.png" for i in range(len(sdg_labels))]

# Cache the map figures
@st.cache_data
def prepare_all_figures():
    all_figures = {}
    for idx, sdg in enumerate(sdg_labels):
        sdg_column = f"SDG{idx + 1}"
        if sdg_column not in color_data.columns:
            st.error(f"Spalte '{sdg_column}' nicht in den Daten gefunden!")
            continue
        filtered_data = color_data[["Country", sdg_column]].dropna()
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

# Sidebar for SDG selection
if "selected_sdg" not in st.session_state:
    st.session_state["selected_sdg"] = sdg_labels[0]

selected_sdg = st.session_state["selected_sdg"]

# Display the selected SDG
st.header(f"Selected SDG: {selected_sdg}")

# Render the map
st.plotly_chart(all_figures[selected_sdg], use_container_width=True)

# Generate SDG image buttons with clickable functionality
cols = st.columns(len(sdg_labels))
for idx, col in enumerate(cols):
    with col:
        st.image(sdg_images[idx], use_column_width=True, caption=sdg_labels[idx])
        if st.button(f"Select {sdg_labels[idx]}", key=f"sdg_button_{idx}"):
            st.session_state["selected_sdg"] = sdg_labels[idx]
            st.experimental_rerun()
