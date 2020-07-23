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

#map stuff##############################################################################################################

# Input data.
with open("new_london_p.json", 'r') as f: #london_p_footfall_sales.json, london_p.json
    data = json.load(f)
marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']


def get_style(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"]["Footfall"] > item][-1] #area_hectares
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)


def get_info(feature=None):
    header = [html.H4("London")]
    if not feature:
        return header + ["Hoover over map"]
    return header + [html.B(feature["properties"]["Name"]), html.Br(),
                     "{} per hour".format(feature["properties"]["Footfall"])]


# Create colorbar.
ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
geojson = dlx.geojson(data, id="geojson", defaultOptions=options, style=get_style)
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

########################################################################################################################

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Miss Marple (Demo)',
                        className='nine columns',
                        style={"margin-left":"15px"}),
                html.Img(
                    src="https://ih1.redbubble.net/image.335413266.9826/flat,128x,075,f-pad,128x128,f8f8f8.u2.jpgsdsfsdfds",
                    className='three columns',
                    style={
                        'height': '15%',
                        'width': '15%',
                        'float': 'right',
                        'position': 'relative',
                        'margin-top': 10,
                    },
                )
            ], className="row"
        ),

        html.Div(
            [
            html.Div([
                dcc.Slider(
                    min=0,
                    max=9,
                    marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                    value=5,
                ),

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
                html.Div(id='radio_output', style={"margin-left":"7px"}), #html.Div

                dcc.Dropdown(
                    options=[
                        {'label': 'Something else 2', 'value': 'Something_else_2'},
                        {'label': 'Something else', 'value': 'Something_else'},
                        {'label': 'Other', 'value': 'Other'}
                    ],
                    value='Other',
                    style={"margin-left":"7px"}
                ),

                dcc.Dropdown(
                    options=[
                        {'label': 'Something else 2', 'value': 'Something_else_2'},
                        {'label': 'Something else', 'value': 'Something_else'},
                        {'label': 'Other', 'value': 'Other'}
                    ],
                    value=['Something_else', 'Something_else_2'],
                    multi=True,
                    style={"margin-left":"7px"}
                ),

                ], className= 'six columns'
                ),

                html.Div([
                    dl.Map(children=[dl.TileLayer(), geojson, colorbar, info], center=[51.51, -0.083], zoom=12)
                ],
                    style={'width': '95%', 'height': '75vh', 'margin': "auto", "display": "block"}, id="map",
                    className= 'six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)



@app.callback(Output("info", "children"), [Input("geojson", "featureHover")])
def info_hover(feature, teststring):
    print (teststring)
    return get_info(feature)

@app.callback(
    Output(component_id='radio_output', component_property='children'),
    [Input(component_id='radioitems', component_property='value')])
def update_radio(input_value):
    radio_choice = input_value
    return radio_choice

@app.callback(
    Output(component_id='radioitems', component_property='children'),
    [Input(component_id='radioitems', component_property='value')])
def update_map(radio_choice):
    print ("radio_choice",radio_choice)

if __name__ == '__main__':
    app.run_server(debug=True)