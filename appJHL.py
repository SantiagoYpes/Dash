# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Importación dataset y manejo de datos.
df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vR39zCK50jRbeuJonUUGCWGa5t1psOH98nuZrZpZtVUtS8j_EFGg2WwqlTZmSlkjmGI6wK_HIIqKsR3/pub?gid=789094753&single=true&output=csv"
)
df["order_value_EUR"] = df["order_value_EUR"].str.replace(",", "").astype(float)
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
df["profit"] = df["order_value_EUR"] - df["cost"]
print(df.info())

# Configuración de estilos.
colors = {"bg": "#333333", "text": "#ffffff"}
primary_color = "#A1343C"

# Obtener valores únicos de la columna 'category'
unique_categories = df["category"].unique()
category_options = [
    {"label": category, "value": category} for category in unique_categories
]

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    style={
        "background": colors["bg"],
    },
    children=[
        dbc.Row(
            dbc.Col(
                html.H1("TiendaEUR Informes"),
                style={
                    "textAlign": "center",
                    "fontFamily": "Segoe UI",
                    "color": colors["text"],
                },
            ),
            justify="center",
            align="center",
        ),
        dbc.Row(
            justify="center",
            align="center",
            children=[
                dbc.Col(
                    dbc.RadioItems(
                        id="filter_device",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-light",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Todos", "value": "All"},
                            {"label": "PC", "value": "PC"},
                            {"label": "Móviles", "value": "Mobile"},
                            {"label": "Tabletas", "value": "Tablet"},
                        ],
                        value="All",
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="filter_category",
                        options=[{"label": "Todos", "value": "All"}] + category_options,
                        value="All",
                        clearable=False,
                        style={
                            "backgroundColor": "white",
                            "color": "black",
                        },
                    ),
                ),
            ],
            className="radio-group",
        ),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                html.H2("Ganancias por país"),
                                style={
                                    "textAlign": "center",
                                    "fontFamily": "Segoe UI",  # Cambiar la fuente a Segoe UI
                                    "color": colors["text"],
                                },
                            ),
                            justify="center",
                            align="center",
                        ),
                        dcc.Graph(
                            figure={},
                            id="profit_country",
                            style={
                                "border": "2px solid #ffffff",
                                "borderRadius": "15px",
                                "margin-bottom": "16px",
                            },
                        ),
                    ]
                ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                html.H2("Costos según dispositivo"),
                                style={
                                    "textAlign": "center",
                                    "fontFamily": "Segoe UI",
                                    "color": colors["text"],
                                },
                            ),
                            justify="center",
                            align="center",
                        ),
                        dcc.Graph(
                            figure={},
                            id="cost_device",
                            style={
                                "border": "2px solid #ffffff",
                                "borderRadius": "15px",
                                "margin-bottom": "16px",
                            },
                        ),
                    ]
                ),
            ]
        ),
    ],
)


# Add controls to build the interaction
@callback(
    Output(component_id="profit_country", component_property="figure"),
    Input(component_id="filter_device", component_property="value"),
)
def update_profit_country(device_type):
    if device_type == "All":
        fig = px.histogram(
            df,
            x="country",
            y="profit",
            histfunc="sum",
            color_discrete_sequence=[primary_color],
        )
        return fig
    filtered_df = df[df["device_type"] == device_type]
    fig = px.histogram(
        filtered_df,
        x="country",
        y="profit",
        histfunc="sum",
        color_discrete_sequence=[primary_color],
    )
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id="cost_device", component_property="figure"),
    Input(component_id="filter_category", component_property="value"),
)
def update_profit_country(category):
    if category == "All":
        pie_fig = px.pie(
            df,
            values="cost",
            names="device_type",
            color_discrete_sequence=px.colors.sequential.RdBu,
        )
        return pie_fig
    filtered_df = df[df["category"] == category]
    pie_fig = px.pie(
        filtered_df,
        values="cost",
        names="device_type",
        color_discrete_sequence=px.colors.sequential.RdBu,
    )
    return pie_fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
