import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# File paths
DATA_PATH = 'Data/SDR2024-data.xlsx'
ASSETS_PATH = Path('assets')

# Load data
def load_data():
    # Load the dataset into a DataFrame
    data = pd.ExcelFile(DATA_PATH)  # Load the Excel file
    return data

data = load_data()

# Debugging: Check available sheet names
st.sidebar.write("### Available Sheets")
st.sidebar.write(data.sheet_names)

# Ensure the correct sheet name is used
sheet_name = "Global View"  # Adjust if necessary
if sheet_name not in data.sheet_names:
    st.error(f"Sheet '{sheet_name}' not found. Available sheets: {data.sheet_names}")
else:
    map_data = pd.read_excel(DATA_PATH, sheet_name=sheet_name)

    # Set up the Streamlit app
    st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")
    st.title("🌍 Sustainable Development Goals Dashboard")

    # World map visualization
    st.write("## Global View")
    fig = px.choropleth(
        map_data,
        locations="Country",
        locationmode="country names",
        color="SDG Progress",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Viridis,
        title="Global SDG Progress"
    )
    st.plotly_chart(fig, use_container_width=True)

    # SDG-specific visualizations
    st.write("## Explore Individual SDGs")
    sdg_options = [f"SDG {i}" for i in range(1, 18)]
    selected_sdg = st.selectbox("Select an SDG to view details:", sdg_options)

    if selected_sdg in map_data.columns:
        fig_sdg = px.choropleth(
            map_data,
            locations="Country",
            locationmode="country names",
            color=selected_sdg,
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Progress on {selected_sdg}"
        )
        st.plotly_chart(fig_sdg, use_container_width=True)
    else:
        st.write("No data available for the selected SDG.")

    # Explanation
    st.sidebar.title("Legend")
    st.sidebar.write("- **Goal Achievement:** Green\n- **Challenges remain:** Yellow\n- **Significant challenges:** Orange\n- **Major challenges:** Red\n- **Insufficient data:** Grey")

    # Add an upload option for future expansion
    st.sidebar.write("### Upload new data")
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    if uploaded_file:
        data = pd.ExcelFile(uploaded_file)
        st.sidebar.success("Data updated successfully!")
