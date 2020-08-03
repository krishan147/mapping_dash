# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
from dash_leaflet import express as dlx
import dash_leaflet as dl
import dash_auth
from dash.dependencies import Output, Input
from datetime import datetime as dt

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# krishan. kinda working. slowly delete stuff and then move stuff...

with open("new_london_p.json", 'r') as f:
    data = json.load(f)
marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

app.layout = html.Div(
    html.Div([
            dbc.Row([
            html.Div(dbc.Col([
                dcc.Dropdown(
                        id = "radioitems",
                        options=[
                            {'label': 'Footfall', 'value': 'Footfall'},
                            {'label': 'Total_Sales', 'value': 'Total_Sales'},
                            {'label': 'P&G_Sales', 'value': 'P&G_Sales'},
                            {'label': 'Unilever_Sales', 'value': 'uni_Sales'},
                            {'label': 'J&J_Sales', 'value': 'J&J_Sales'},
                            {'label': 'Supermarket Sales', 'value': 'Supermarket_Sales'},
                            {'label': 'Beauty Retailer Sales', 'value': 'Beauty_Retailer_Sales'},
                            {'label': 'No. of Supermarkets', 'value': 'No_of_Supermarkets'},
                            {'label': 'No. of Beauty Retailers', 'value': 'No_of_Beauty_Retailers'},
                            {'label': 'No. of Hairdressers', 'value': 'No_of_Hairdressers'},
                        ],
                        value='Footfall',
                        style={"margin-left":"7px"},
                    ),

                html.Div(id='radio_output', style={"margin-left":"7px"}),

                ]), className= 'six columns'
                ),
                html.Div(dbc.Col([], id="map")),
                html.Div(dbc.Col([], id="info"))
            ]),
        html.H1('thishtishtis'),
        ],
    )
)

@app.callback(
    Output(component_id='radio_output', component_property='children'),
    [Input(component_id='radioitems', component_property='value')])
def update_radio(input_value):
    if input_value != None:

        print ("update_radio", input_value)

        def get_style(feature):
            color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"][input_value] > item][-1]
            return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

        options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
        geojson = dlx.geojson(data, id="geojson", defaultOptions=options, style=get_style)

        return html.Div([
                    dl.Map(children=[dl.TileLayer(), geojson], center=[51.51, -0.083], zoom=11)
                ],
                    style={'width': '95%', 'height': '75vh', 'margin': "auto", "display": "block"}, id="map"
                )

@app.callback([Output("info", "children")], [Input("geojson", "featureHover"), Input(component_id='radioitems', component_property='value')])
def info_hover(feature, input_value):

    print("info_hover", input_value)
    figure = feature["properties"][input_value]
    postcode = feature["properties"]["Name"]

    if "Total_Sales" == input_value or "Supermarket_Sales" == input_value:
        figure = "£" + str(feature["properties"][input_value])
    elif "Footfall" in input_value:
        figure = str(feature["properties"][input_value]) + " per hour"
    else:
        figure = str(figure)

    return [html.Div(
        [
            html.H4(str(figure)),
            html.H4(str(postcode))
        ],
        id="info")
    ]

if __name__ == '__main__':
    app.run_server(debug=True)