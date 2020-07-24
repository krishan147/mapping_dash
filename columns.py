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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

#map stuff##############################################################################################################

with open("new_london_p.json", 'r') as f: #london_p_footfall_sales.json, london_p.json
    data = json.load(f)
marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

def get_style(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"]["Footfall"] > item][-1] #area_hectares
    that = dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
    return that

def get_info(feature=None):
    header = [html.H4("London")]
    if not feature:
        return header + ["Hoover over map"]
    return header + [html.B(feature["properties"]["Name"]), html.Br(),
                     "{} per hour".format(feature["properties"]["Footfall"])]

ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
geojson = dlx.geojson(data, id="geojson", defaultOptions=options, style=get_style)

info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

########################################################################################################################

app.layout = html.Div(
    html.Div([
        html.Div(
            [
            html.Div([
                dcc.RadioItems(
                        id = "radioitems",
                        options=[
                            {'label': 'Footfall', 'value': 'Footfall'},
                            {'label': 'Total_Sales', 'value': 'Total_Sales'},
                            {'label': 'Supermarket Sales', 'value': 'Supermarket_Sales'},
                            {'label': 'Beauty Retailer Sales', 'value': 'Beauty_Retailer_Sales'},
                            {'label': 'No. of Supermarkets', 'value': 'No_of_Supermarkets'},
                            {'label': 'No. of Beauty Retailers', 'value': 'No_of_Beauty_Retailers'},
                            {'label': 'No. of Hairdressers', 'value': 'No_of_Hairdressers'},
                        ],
                        value='footfall',
                        style={"margin-left":"15px"},
                    ),

                html.Div(id='radio_output')
                ], className= 'six columns'
                ),
                html.Div([],id="map"),
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

@app.callback(
    Output(component_id='radio_output', component_property='children'),
    [Input(component_id='radioitems', component_property='value')])
def update_radio(input_value):
    if input_value != None:

        def get_style(feature):
            color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"][input_value] > item][-1]
            return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

        def get_info(feature=None):
            header = [html.H4("London")]
            if not feature:
                return header + ["Hoover over map"]
            return header + [html.B(feature["properties"]["Name"]), html.Br(),
                             "{} per hour".format(feature["properties"][input_value])]

        options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
        geojson = dlx.geojson(data, id="geojson", defaultOptions=options, style=get_style)

        info = html.Div(children=get_info(), id="info", className="info",
                        style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

        return html.Div([
                    dl.Map(children=[dl.TileLayer(), geojson, info], center=[51.51, -0.083], zoom=12)
                ],
                    style={'width': '95%', 'height': '75vh', 'margin': "auto", "display": "block"}, id="map",
                    className= 'six columns'
                )

@app.callback(Output("info", "children"), [Input("geojson", "featureHover")])


# the below doesnt work for some reason krishan
def info_hover(feature):

    def get_info(feature=None):
        header = [html.H4("London")]
        if not feature:
            return header + ["Hoover over map"]
        return header + [html.B(feature["properties"]["Name"]), html.Br(),
                         "{} per hour".format(feature["properties"]["Footfall"])]

    info = html.Div(children=get_info(), id="info", className="info",
                    style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

    return html.Div([info])

    # return html.Div([
    #                 dl.Map(children=[info], center=[51.51, -0.083], zoom=12)
    #             ])

if __name__ == '__main__':
    app.run_server(debug=True)