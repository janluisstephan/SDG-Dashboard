import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback_context
import os

# Daten laden
data_path = '/Users/luisstephan/Desktop/Studium/Wirtschaftsinformatik/Python/Projekte/Data/SDR2024-data.xlsx'
sdg_images_path = '/Users/luisstephan/Desktop/Studium/Wirtschaftsinformatik/Python/Projekte/Data/sdg_images/'

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
color_meanings = {
    "green": "Goal Achievement",
    "yellow": "Challenges remain",
    "orange": "Significant challenges",
    "red": "Major challenges",
    "grey": "Insufficient data"
}

# Dash-Anwendung erstellen
app = Dash(__name__)

# Layout der Dash-App
app.layout = html.Div([
    html.Div([
        html.H1("Sustainable Development Goals Dashboard", style={"textAlign": "center", "fontFamily": "Arial, sans-serif", "color": "#333", "marginBottom": "20px"}),
        html.H3(id="current-sdg", style={"textAlign": "center", "fontFamily": "Arial, sans-serif", "color": "#333", "marginBottom": "20px"}),
    ], style={"backgroundColor": "#f9f9f9", "padding": "10px"}),

    html.Div([
        html.Div([
            dcc.Graph(id="sdg-map", config={"displayModeBar": False}, style={"height": "600px"}),
        ], style={"width": "75%", "display": "inline-block", "padding": "10px", "backgroundColor": "#ffffff", "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)", "position": "relative"}),

        html.Div([
            html.Div(id="country-trend", style={"fontSize": "14px", "marginTop": "10px", "color": "#333"}),
            html.Div([
                html.P("Goal Achievement", style={"color": "#2ca02c", "margin": "5px", "fontSize": "14px"}),
                html.P("Challenges remain", style={"color": "#ffdd57", "margin": "5px", "fontSize": "14px"}),
                html.P("Significant challenges", style={"color": "#ffa500", "margin": "5px", "fontSize": "14px"}),
                html.P("Major challenges", style={"color": "#d62728", "margin": "5px", "fontSize": "14px"}),
                html.P("Insufficient data", style={"color": "#808080", "margin": "5px", "fontSize": "14px"}),
                html.Hr(),
                html.P("Trend Explanation:", style={"fontWeight": "bold"}),
                html.P("↑ On track or maintaining achievement", style={"color": "#2ca02c", "margin": "5px", "fontSize": "14px"}),
                html.P("➚ Moderately Increasing", style={"color": "#ffa500", "margin": "5px", "fontSize": "14px"}),
                html.P("→ Stagnating", style={"color": "#ffdd57", "margin": "5px", "fontSize": "14px"}),
                html.P("↓ Decreasing", style={"color": "#d62728", "margin": "5px", "fontSize": "14px"})
            ], style={"marginTop": "20px"})
        ], style={"width": "20%", "display": "inline-block", "padding": "10px", "backgroundColor": "#f9f9f9", "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)", "verticalAlign": "top", "marginLeft": "10px"})
    ], style={"display": "flex", "justifyContent": "space-between"}),

    html.Div([
        html.Div([
            html.Img(
                src=f"assets/{i + 1}.png",
                id=f"sdg-button-{i}",
                style={"margin": "10px", "cursor": "pointer", "width": "80px" if i != 6 else "100px"}
            ) for i in range(len(sdg_labels))
        ], style={"textAlign": "center", "marginTop": "20px"}),
    ])
], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f4f4f4", "padding": "20px"})

# Initial States
initial_sdg_index = 0
current_sdg = color_columns[initial_sdg_index]
current_trend = trend_columns[initial_sdg_index]

# Callback zur Aktualisierung der Karte und der Legende
@app.callback(
    [Output("sdg-map", "figure"), Output("country-trend", "children"), Output("current-sdg", "children")],
    [Input(f"sdg-button-{i}", "n_clicks_timestamp") for i in range(len(sdg_labels))] + [Input("sdg-map", "clickData")]
)
def update_map_and_trend(*args):
    ctx = callback_context

    global current_sdg, current_trend
    trend_label = "Select a country to see the trend."
    current_sdg_label = no_update  # Do not update by default

    if ctx.triggered:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id.startswith("sdg-button"):
            # Update SDG and Trend when an SDG button is clicked
            button_index = int(triggered_id.split("-")[-1])
            current_sdg = color_columns[button_index]
            current_trend = trend_columns[button_index]
            current_sdg_label = f"Current SDG: {sdg_labels[button_index]}"
            trend_label = "Select a country to see the trend."

        elif triggered_id == "sdg-map":
            # Update only the trend when a country is clicked
            click_data = args[-1]
            if click_data:
                country_name = click_data["points"][0]["location"]
                trend_value = color_data.loc[color_data["Country"] == country_name, current_trend].values
                if trend_value:
                    trend_symbol = trend_value[0]
                    trend_image = {
                        '↑': 'assets/up.png',
                        '↓': 'assets/down.png',
                        '➚': 'assets/right-up.png',
                        '→': 'assets/right.png'
                    }.get(trend_symbol, 'assets/no_trend.png')
                    trend_label = html.Div([
                        html.P(f"Country: {country_name}", style={"fontWeight": "bold"}),
                        html.Img(src=trend_image, style={"width": "30px", "height": "30px"})
                    ])

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
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#f9f9f9",
        plot_bgcolor="#f9f9f9",
        showlegend=False
    )

    return fig, trend_label, current_sdg_label



# Anwendung starten
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
