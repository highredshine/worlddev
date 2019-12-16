import plotly.graph_objects as go
import pandas as pds

COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

def query(country_code, indicator):
    sql = """
        SELECT country_name, indicator, year, value
        FROM `worlddev.wdi.main`
        WHERE country_code = @country_code AND indicator = @indicator
    """
    config = {
        'query': {
            'parameterMode': 'NAMED',
            'queryParameters': [
                {
                    'name': 'country_code',
                    'parameterType': {'type': 'STRING'},
                    'parameterValue': {'value': country_code}
                },
                {
                    'name': 'indicator',
                    'parameterType': {'type': 'STRING'},
                    'parameterValue': {'value': indicator}
                }
            ]
        }
    }
    df = pds.read_gbq(sql, configuration=config, project_id='worlddev')
    return df

def visualize(df, stack=False):
    sources = ['value']
    x = df['year']
    name = df['indicator'][0]
    fig = go.Figure()
    for i, s in enumerate(sources):
        fig.add_trace(go.Scatter(x=x, y=df[s], mode='lines', name=name,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))

    fig.update_layout(template='plotly_dark',
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Value',
                      xaxis_title='Year')
    return fig


