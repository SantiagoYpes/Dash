# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR39zCK50jRbeuJonUUGCWGa5t1psOH98nuZrZpZtVUtS8j_EFGg2WwqlTZmSlkjmGI6wK_HIIqKsR3/pub?gid=789094753&single=true&output=csv')
df1['order_value_EUR'] = df1['order_value_EUR'].str.replace(',', '').astype(float)
df1['date'] = pd.to_datetime(df1['date'], format='%m/%d/%Y')
print(df1.info())

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    
    dash_table.DataTable(
                data=df1.to_dict('records'),
                page_size=6,
                style_table={'overflowX': 'auto'}
            ),
    html.Div([
        
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Population', 'value': 'pop'},
                    {'label': 'Life Expectancy', 'value': 'lifeExp'},
                    {'label': 'GDP per Capita', 'value': 'gdpPercap'}
                ],
                value='lifeExp',
                id='controls-and-radio-item'
            ),
            dcc.Graph(
                figure={},
                id='controls-and-graph'
            )
            
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Population', 'value': 'pop'},
                    {'label': 'Life Expectancy', 'value': 'lifeExp'},
                    {'label': 'GDP per Capita', 'value': 'gdpPercap'}
                ],
                value='lifeExp',
                id='controls-and-radio-item'
            ),
            dcc.Graph(
                figure={},
                id='controls-and-graph'
            )
        ], style={'width': '48%', 'height':'20%','display': 'inline-block', 'vertical-align': 'top'})
    ])
])
# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
