import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Daten laden
data_path = 'Data/SDR2024-data.xlsx'
sdg_images_path = 'assets/'

sdg_data = pd.read_excel(data_path, sheet_name='Full Database', engine='openpyxl')
color_data = pd.read_excel(data_path, sheet_name='Overview', engine='openpyxl')

# SDG-Spalten identifizieren
sdg_columns = [col for col in sdg_data.columns if "Goal" in col and "Score" in col]
color_columns = [col for col in color_data.columns if col.startswith("SDG")]

# Dynamische Identifikation der Trendspalten
trend_columns = [
    color_data.columns[color_data.columns.get_loc(col) + 1] if color_data.columns.get_loc(col) + 1 < len(color_data.columns) else None
    for col in color_columns
]

# SDG-Labels vorbereiten
sdg_labels = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]

# Farbcodierungen und Bedeutungen
color_mapping = {
    "green": "#2ca02c",
    "yellow": "#ffdd57",
    "orange": "#ffa500",
    "red": "#d62728",
    "grey": "#808080"
}

# Initial States
initial_sdg_index = 0
current_sdg = color_columns[initial_sdg_index]
current_trend = trend_columns[initial_sdg_index]

# Streamlit Layout
st.title("Sustainable Development Goals Dashboard")
st.subheader("Select an SDG to view country performance and trends.")

# Update the map based on the current SDG
filtered_data = color_data[["Country", current_sdg]].dropna()
filtered_data.rename(columns={current_sdg: "Color"}, inplace=True)

fig = px.choropleth(
    filtered_data,
    locations="Country",
    locationmode="country names",
    color="Color",
    hover_name="Country",
    title="",
    color_discrete_map=color_mapping
)

fig.update_traces(marker_line_width=0)
fig.update_layout(
    margin={"r": 5, "t": 5, "l": 5, "b": 5},  # Reduzierte Ränder
    paper_bgcolor="#f9f9f9",
    plot_bgcolor="#f9f9f9",
    showlegend=False,
    dragmode=False  # Macht die Karte statisch
)

st.plotly_chart(fig, use_container_width=True)

# Trendanzeige bei Länder-Auswahl
st.write("### Country Trends")
selected_country = st.selectbox("Select a country to see the trend", filtered_data["Country"].unique())

if selected_country:
    trend_value = color_data.loc[color_data["Country"] == selected_country, current_trend].values
    if trend_value.size > 0:
        trend_symbol = trend_value[0]
        trend_description = {
            '↑': 'On track or maintaining achievement',
            '↓': 'Decreasing',
            '➚': 'Moderately Increasing',
            '→': 'Stagnating'
        }.get(trend_symbol, 'No trend available')
        st.write(f"**Country:** {selected_country}")
        st.write(f"**Trend:** {trend_symbol} - {trend_description}")
    else:
        st.write("No trend data available for the selected country.")

# Legende der Farbcodierungen
st.write("### Legend")
st.write("**Color Codes:**")
st.markdown(
    """ 
    - <span style='color:#2ca02c;'>**Green:** Goal Achievement</span>
    - <span style='color:#ffdd57;'>**Yellow:** Challenges remain</span>
    - <span style='color:#ffa500;'>**Orange:** Significant challenges</span>
    - <span style='color:#d62728;'>**Red:** Major challenges</span>
    - <span style='color:#808080;'>**Grey:** Insufficient data
    """,
    unsafe_allow_html=True
)

st.write("**Trend Explanation:**")
st.markdown(
    """ 
    - **↑:** On track or maintaining achievement
    - **➚:** Moderately Increasing
    - **→:** Stagnating
    - **↓:** Decreasing
    """
)

# SDG-Knöpfe mit Icons
st.write("### Select SDG via Icons")
sdg_icons = st.columns(len(sdg_labels))

for i, label in enumerate(sdg_labels):
    icon_path = os.path.join(sdg_images_path, f"{i + 1}.png")
    with sdg_icons[i]:
        if st.button(
            "",
            help=label,
            key=f"sdg_button_{i}"
        ):
            current_sdg = color_columns[i]
            current_trend = trend_columns[i]
            st.experimental_rerun()
        st.image(icon_path, use_column_width=True)
