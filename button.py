import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div([

    html.Div([

        dcc.Input(id='input', value='Enter something here!', type='text'),
        html.Div(id='output')
    ]),
    html.Div([
        dcc.RadioItems(
            id="input2",
            options=[
                {'label': 'Footfall', 'value': 'Footfall'},
                {'label': 'Sales', 'value': 'Sales'},
                {'label': 'Other', 'value': 'Other'}
            ],
            value='Footfall',
            style={"margin-left": "15px"},
        ),
        html.Div(id='output2')
    ])
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    print (input_data)
    return 'Input: "{}"'.format(input_data)

@app.callback(
    Output(component_id='output2', component_property='children'),
    [Input(component_id='input2', component_property='value')]
)
def update_value2(input_data2):
    print (input_data2)
    return 'Input: "{}"'.format(input_data2)

if __name__ == '__main__':
    app.run_server(debug=True)