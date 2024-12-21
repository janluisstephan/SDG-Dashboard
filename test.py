import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set up the Streamlit app (must be the first Streamlit command)
st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")

# File paths
DATA_PATH = 'Data/SDR2024-data.xlsx'
ASSETS_PATH = Path('assets')

# Load data
def load_data():
    # Load the dataset into a DataFrame
    data = pd.ExcelFile(DATA_PATH)  # Load the Excel file
    return data

data = load_data()

# Ensure the correct sheet name is used
sheet_name = "Overview"  # Adjusted based on available sheets
if sheet_name not in data.sheet_names:
    st.error(f"Sheet '{sheet_name}' not found. Available sheets: {data.sheet_names}")
else:
    map_data = pd.read_excel(DATA_PATH, sheet_name=sheet_name)

    # Set default column for color or fallback to first numeric column
    color_column = "SDG Progress" if "SDG Progress" in map_data.columns else None
    if not color_column:
        numeric_columns = map_data.select_dtypes(include=['number']).columns
        if not numeric_columns.empty:
            color_column = numeric_columns[0]
            st.warning(f"Defaulting to first numeric column: {color_column}")
        else:
            st.error("No suitable numeric column found for visualization.")

    if color_column:
        st.title("🌍 Sustainable Development Goals Dashboard")

        # SDG-specific visualizations
        sdg_options = [col for col in map_data.columns if col.startswith("SDG")]
        selected_sdg = st.selectbox("Select an SDG to view on the map:", sdg_options)

        if selected_sdg in map_data.columns:
            # World map visualization for selected SDG
            st.write(f"## Progress on {selected_sdg}")
            fig_sdg = px.choropleth(
                map_data,
                locations="Country",
                locationmode="country names",
                color=selected_sdg,
                hover_name="Country",
                color_continuous_scale=["#e31a1c", "#fd8d3c", "#fecc5c", "#31a354"], # Custom SDG colors
                title=f"Progress on {selected_sdg}"
            )
            st.plotly_chart(fig_sdg, use_container_width=True)
        else:
            st.write("No data available for the selected SDG.")
