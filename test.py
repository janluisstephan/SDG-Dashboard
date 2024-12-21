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

    # Define SDG color mapping based on legend
    sdg_color_mapping = {
        "Goal Achievement": "#31a354",  # Green
        "Challenges remain": "#fecc5c",  # Yellow
        "Significant challenges": "#fd8d3c",  # Orange
        "Major challenges": "#e31a1c",  # Red
        "Insufficient data": "#969696"   # Grey
    }

    # Ensure required columns
    required_columns = ["Country"] + [col for col in map_data.columns if col.startswith("SDG")]
    if not all(col in map_data.columns for col in required_columns):
        st.error("Required columns for the dashboard are missing.")
    else:
        st.title("🌍 Sustainable Development Goals Dashboard")

        # SDG-specific visualizations
        sdg_options = [col for col in map_data.columns if col.startswith("SDG")]
        selected_sdg = st.selectbox("Select an SDG to view on the map:", sdg_options, format_func=lambda x: x.split(": ")[1])

        if selected_sdg in map_data.columns:
            # Map data preparation
            map_data["Category"] = map_data[selected_sdg].map(sdg_color_mapping)

            # World map visualization for selected SDG
            st.write(f"## {selected_sdg.split(': ')[1]}")
            fig_sdg = px.choropleth(
                map_data,
                locations="Country",
                locationmode="country names",
                color=selected_sdg,
                hover_name="Country",
                color_discrete_map=sdg_color_mapping,
                title=f"{selected_sdg.split(': ')[1]}"
            )
            st.plotly_chart(fig_sdg, use_container_width=True)

        # Display SDG legend
        st.write("### Legend")
        st.markdown(
            """
            - **Green:** Goal Achievement  
            - **Yellow:** Challenges remain  
            - **Orange:** Significant challenges  
            - **Red:** Major challenges  
            - **Grey:** Insufficient data  
            """
        )

        # Display SDG icons
        st.write("### Explore Other SDGs")
        st.image([str(ASSETS_PATH / f"{i}.png") for i in range(1, 18)], width=50)

