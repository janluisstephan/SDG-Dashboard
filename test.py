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
    data = pd.read_excel(DATA_PATH, sheet_name=None)  # Load all sheets
    return data

data = load_data()

# Set up the Streamlit app
st.set_page_config(page_title="Sustainable Development Goals Dashboard", layout="wide")
st.title("🌍 Sustainable Development Goals Dashboard")

# Helper function to load image
@st.cache
def load_image(image_name):
    image_path = ASSETS_PATH / image_name
    return str(image_path)

# Select country to view details
country_list = list(data['Dashboard']['Country'].unique())
selected_country = st.selectbox("Select a country to see the trend:", country_list)

# Display country-specific trends
country_data = data['Dashboard'][data['Dashboard']['Country'] == selected_country]
st.write(f"### Trends for {selected_country}")

for sdg in range(1, 18):
    # Load SDG icon
    icon_path = load_image(f"{sdg}.png")

    # Extract data for the SDG
    sdg_data = country_data[country_data['SDG'] == f"SDG {sdg}"]

    # Display SDG icon and trend data
    st.image(icon_path, width=50)
    st.write(f"**SDG {sdg}:** {sdg_data['Trend'].values[0] if not sdg_data.empty else 'No data'}")

# World map visualization
st.write("## Global View")
map_data = data['Global View']  # Assuming sheet contains global data
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

# Explanation
st.sidebar.title("Legend")
st.sidebar.write("- **Goal Achievement:** Green\n- **Challenges remain:** Yellow\n- **Significant challenges:** Orange\n- **Major challenges:** Red\n- **Insufficient data:** Grey")

# Add an upload option for future expansion
st.sidebar.write("### Upload new data")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file:
    data = pd.read_excel(uploaded_file, sheet_name=None)
    st.sidebar.success("Data updated successfully!")
