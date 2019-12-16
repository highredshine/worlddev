import dash_html_components as html


def title():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H1('World Development Indicators')])
    ], className="row", style={
        'textAlign': 'center', 'paddingTop': '3%'
    })