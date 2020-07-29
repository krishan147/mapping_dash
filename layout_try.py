import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls'),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey')  # Define the right element
                                  ])
                                ])
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)