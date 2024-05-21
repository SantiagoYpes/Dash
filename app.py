# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq


df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vR39zCK50jRbeuJonUUGCWGa5t1psOH98nuZrZpZtVUtS8j_EFGg2WwqlTZmSlkjmGI6wK_HIIqKsR3/pub?gid=789094753&single=true&output=csv"
)
df["order_value_EUR"] = df["order_value_EUR"].str.replace(",", "").astype(float)
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
df["profit"] = df["order_value_EUR"] - df["cost"]
print(df.info())


month_names = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

# Configuración de estilos.
colors = {"bg": "#333333", "text": "#ffffff"}
primary_color = "#A1343C"

unique_categories = df["category"].unique()
unique_countries = df["country"].unique()
category_options = [
    {"label": category, "value": category} for category in unique_categories
]

country_options = [
    {"label": country, "value": country} for country in unique_countries
]

df_grouped = df.groupby(df['date'].dt.date).agg({'cost': 'sum'}).reset_index()
df_grouped['date'] = pd.to_datetime(df_grouped['date'])  

fig = px.line(df_grouped, x='date', y='cost', title='Costos diarios a lo largo del tiempo')

scatter_fig = px.scatter(df, x='cost', y='profit', title='Ganancia según el costo')
scatter_fig.update_traces(marker=dict(color=primary_color))


def abbreviate_number(num):
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(num) < 1000.0:
            return "{:.2f}{}".format(num, unit)
        num /= 1000.0
    return "{:.2f}{}".format(num, 'T')

total_profit_pc = df[df['device_type'] == 'PC']['profit'].sum()
formatted_profit_pc = abbreviate_number(total_profit_pc)

total_profit = df['profit'].sum()
formatted_profit = abbreviate_number(total_profit)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



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
                    dbc.Card(
                        [
                            dbc.CardHeader("Ganancias totales"),
                            dbc.CardBody(
                                [
                                    html.H4(formatted_profit, className="card-title"),
                                ]
                            ),
                        ],
                        style={
                            "textAlign": "center",
                            "fontFamily": "Segoe UI",
                    
                        },
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Total de ganancias en PC"),
                            dbc.CardBody(
                                [
                                    html.H4(formatted_profit_pc, className="card-title"),
                                ]
                            ),
                        ],
                        style={
                            "textAlign": "center",
                            "fontFamily": "Segoe UI",
                    
                        },
                    )
                ),                
            ],
            
        ),
        html.Br(),
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
        
        dbc.Row(
            justify="center",
            align="center",
            children=[
                dbc.Col(
                    dcc.Dropdown(
                        id="select",
                        multi=True,
                        placeholder="Selecciona un país",
                        
                        options=  country_options,
                        style={
                            "backgroundColor": "white",
                            "color": "black",
                        },
                    ),  
                ),
                dbc.Col(
                    dcc.Slider(
                        id='date-slider',
                        min=0,
                        max=len(df_grouped) - 1,
                        value=len(df_grouped) - 1,
                        tooltip={"placement": "bottom", "always_visible": True},
                        included=True,
                        
                    ),style={  
                            "color": primary_color,
                    },
                    
                ),
            ],
            className="slider-group",
        ),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                html.H2("Ganancia según el costo"),
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
                            figure=scatter_fig,
                            id="profit_vs_cost",
                            style={
                                "border": "2px solid #ffffff",
                                "borderRadius": "15px",
                                "margin-bottom": "16px",
                            },
                        ),
                    ]),
                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                html.H2("Costos en el tiempo"),
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
                            figure=fig,
                            id="cost_datetime",
                            style={
                                "border": "2px solid #ffffff",
                                "borderRadius": "15px",
                                "margin-bottom": "16px",
                            },
                        ),
                        dbc.RadioItems(
                        id="filter_period",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-light",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Todo", "value": "All"},
                            {"label": "Año", "value": "Year"},
                            {"label": "Semestre", "value": "Quarter"},
                            {"label": "Mes", "value": "Month"},
                        ],
                        value="All",
                    ),
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.H3("TiendaEUR Dataset"),
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
            dbc.Col(
                dash_table.DataTable(df.to_dict('records'), page_size=10,style_table={'overflowX': 'auto'},),
                style={
                    "textAlign": "center",
                    "fontFamily": "Segoe UI",
                },
            ),
            justify="center",
            align="center",
        ),
    ],
)

@callback(
    Output(component_id="profit_vs_cost", component_property="figure"),
    Input(component_id="select", component_property="value"),
)
def update_scatter(selected_countries):
    if (selected_countries is None) or (len(selected_countries) == 0):
        selected_countries = []  
        filtered_df = df
    else:
        filtered_df = df[df['country'].isin(selected_countries)]
    scatter_fig = px.scatter(filtered_df, x='cost', y='profit', title='Ganancia según el costo')
    scatter_fig.update_traces(marker=dict(color=primary_color))
    return scatter_fig


@callback(
    Output('cost_datetime', 'figure'),
    [Input('date-slider', 'value'), Input('filter_period', 'value')]
)
def update_time_cost(selected_day, period):
    if period == "All":
        filtered_df = df_grouped[df_grouped['date'] <= df_grouped['date'].iloc[selected_day]]
    elif period == "Year":
        filtered_df = df_grouped.groupby(df_grouped['date'].dt.year)['cost'].sum().reset_index()
    elif period == "Quarter":
        filtered_df = df_grouped.groupby(df_grouped['date'].dt.quarter)['cost'].sum().reset_index()
    elif period == "Month":
        filtered_df = df_grouped.groupby(df_grouped['date'].dt.month)['cost'].sum().reset_index()
        filtered_df['date'] = filtered_df['date'].map(month_names)
    fig = px.line(filtered_df, x='date', y='cost')
    fig.update_traces(line=dict(color=primary_color)) 
    fig.update_layout(
        title={
            'x':0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title='Fecha',
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title='Costo'
        )
    )
    return fig

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
