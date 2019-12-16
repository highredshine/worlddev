import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from main import main_page
from about import about_page
from details import details_page
from common import address

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

# @app.callback(Output('page-1-content', 'children'),
#               [Input('page-1-dropdown', 'value')])
# def page_1_dropdown(value):
#     return 'You have selected "{}"'.format(value)


# @app.callback(Output('page-2-content', 'children'),
#               [Input('page-2-radios', 'value')])
# def page_2_radios(value):
#     return 'You have selected "{}"'.format(value)


# Update the index
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
    app.run_server(debug=True, host=address())