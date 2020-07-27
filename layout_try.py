import dash_bootstrap_components as dbc
import dash_html_components as html
import dash

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns"))
            ]
        ),
    ]
)


app.layout = html.Div(html.Div([row]))

if __name__ == '__main__':
    app.run_server(debug=True)