import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import main_page
from about import about_page
from details import details_page

import visuals

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

@app.callback(Output('byIndicator-graph', 'figure'),
             [Input('country-dropdown-byIndicator', 'value'),
              Input('indicator-dropdown-byIndicator', 'value')])
def byIndicator(country_code, indicators):
    return visuals.callback_byIndicator(country_code, indicators)


@app.callback(Output('byCountries-graph', 'figure'),
             [Input('country-dropdown-byCountries', 'value'),
              Input('indicator-dropdown-byCountries', 'value')])
def byCountries(country_codes, indicator):
    return visuals.callback_byCountries(country_codes, indicator)
    

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_page()
    if pathname == '/about':
         return about_page()
    elif pathname == '/details':
         return details_page(app)
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')