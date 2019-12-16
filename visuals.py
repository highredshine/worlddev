import plotly.graph_objects as go
import pandas as pds
from common import credentials, color

def query(cache, country_code, indicator):
    sql = """
        SELECT country_name as country, indicator, year, value
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
    key = country_code+'-'+indicator
    if key not in cache:
        cache[key] = pds.read_gbq(sql, 
                                  configuration=config, 
                                  project_id='worlddev', 
                                  credentials=credentials())
    return cache[key]

    
def visualize(queries, by):
    categories = [] 
    earliest = queries[0]['year'].min()
    latest = queries[0]['year'].max()
    for query in queries:
        first_year = query['year'].min()
        last_year = query['year'].max()
        if earliest < first_year:
            earliest = first_year
        if latest > last_year:
            latest = last_year
        categories.append(query[by][0])
    for i in range(len(queries)):
        queries[i] = queries[i][(queries[i].year >= earliest) & (queries[i].year <= latest)]
        if by == 'indicator':
            vals = queries[i]['value']
            queries[i]['value'] = (vals-vals.mean())/vals.std()
    fig = go.Figure()
    for i in range(len(queries)):
        query = queries[i]
        fig.add_trace(go.Scatter(x=query['year'], y=query['value'], name=categories[i],
                                 mode='lines', 
                                 line={'width': 2, 'color': color()},
                                 fill='none'))
    fig.update_layout(template='plotly_dark',
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='Value',
                      xaxis_title='Year')
    return fig


def callback_byIndicator(cache, country_code, indicators):
    queries = []
    for indicator in indicators:
        queries.append(query(cache, country_code, indicator))
    return visualize(queries, 'indicator')


def callback_byCountries(cache, country_codes, indicator):
    queries = []
    for country_code in country_codes:
        queries.append(query(cache, country_code, indicator))
    return visualize(queries, 'country')
