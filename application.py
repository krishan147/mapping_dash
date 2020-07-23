import dash
import dash_html_components as html
import json
import dash_leaflet as dl
from dash.dependencies import Output, Input
from dash_leaflet import express as dlx
import dash_core_components as dcc

# Input data.
with open("usa.json", 'r') as f:
    data = json.load(f)
marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']


def get_style(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"]["density"] > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + ["Hoover over a state"]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]

# Create colorbar.
ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Create geojson.
options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
geojson = dlx.geojson(data, id="geojson", defaultOptions=options, style=get_style)
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

infotwo = html.Div(children=get_info(), id="infotwo", className="info",
                style={"position": "absolute", "top": "50px", "right": "50px", "z-index": "1000"})

# Create app.
app = dash.Dash(prevent_initial_callbacks=True)

app.layout = html.Div([

    html.Div([
        dcc.RadioItems(
            id="radioitems",
            options=[
                {'label': 'Footfall', 'value': 'Footfall'},
                {'label': 'Total_Sales', 'value': 'Total_Sales'},
            ],
            #value='footfall',
            style={"margin-left": "15px"},
        ),
        html.Div(id='radio_output', style={"margin-left": "15px"}),  # html.Div

    ], className='six columns'
    ),

    html.Div([
        dl.Map(children=[dl.TileLayer(), geojson, colorbar, info], center=[39, -98], zoom=4)],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")
])


@app.callback(Output("info", "children"), [Input("geojson", "featureHover")])
def info_hover(feature):
    return get_info(feature)


@app.callback(Output("radio_output", "children"), [Input("radioitems", "value")]) # component_id, component_property
def update_radio(input_value):
    print (input_value)
    return input_value


if __name__ == '__main__':
    app.run_server()