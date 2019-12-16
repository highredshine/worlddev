import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from common import title, cache
import visuals
import cluster

def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[
        dcc.Markdown('''
            "History followed different courses for different peoples 
            because of differences among peoples' environments, 
            not because of biological differences among peoples themselves.
            " ― Jared Diamond, Guns, Germs and Steel: The Fates of Human Societies
            #
            This project was inspired from the quote above. 
            The human civilization has developed for about 6000 years now, and 
            the current world now is divided into so-called 'developed' and 'developing' countries.
            Using World Bank's latest data on 'World Development Indicators', 
            this project aims to understand what it means to be a developed or developing country,
            or what we can do for developing ones to become developed.
        ''')], className="row", style={
        'textAlign': 'center'
    })

def visualization(countries_dict, indicators_dict):
    """
    Returns overall project description in markdown
    """
    initial_country_value_1 = 'WLD'
    initial_country_value_2 = ['WLD','USA','CHN']
    initial_indicator_value_1 = ['Access to electricity', 
                                 'GDP', 
                                 'Literacy rate', 
                                 'Taxes on income']
    initial_indicator_value_2 = 'GDP'
    return html.Div(children=[
        dcc.Markdown('''
            ### Observing the Indicators
            The data consists all the annual time series data of numerous indicators 
            gathered from all around the world. The default plot shows the world average of some of the
            representative indicators such as electricity access. The two dashboard shows two different ways to interact with the data:
            #### choose one country and pick one or more indicators to understand the development of the country.
            ##### (in this case, the query normalizes the values to show different indicators in the same scale)
        '''),
        dcc.Dropdown(
            id='country-dropdown-byIndicator',
            options=[{'label': k, 'value': v} for k, v in countries_dict.items()],
            value=initial_country_value_1,
            placeholder="Select a country"
        ),
        dcc.Dropdown(
            id='indicator-dropdown-byIndicator',
            options=[{'label': k, 'value': k} for k in indicators_dict],
            value=initial_indicator_value_1,
            multi=True,
            placeholder="Select an indicator"
        ),
        dcc.Graph(id='byIndicator-graph', figure=visuals.callback_byIndicator(initial_country_value_1,initial_indicator_value_1)),
        dcc.Markdown('''
            #### choose one indicator and pick one or more countries to understand the relevance of the indicator.
        '''),
        dcc.Dropdown(
            id='country-dropdown-byCountries',
            options=[{'label': k, 'value': v} for k, v in countries_dict.items()],
            value=initial_country_value_2,
            multi=True,
            placeholder="Select a country"
        ),
        dcc.Dropdown(
            id='indicator-dropdown-byCountries',
            options=[{'label': k, 'value': k} for k in indicators_dict],
            value=initial_indicator_value_2,
            placeholder="Select an indicator"
        ),
        dcc.Graph(id='byCountries-graph', figure=visuals.callback_byCountries(initial_country_value_2,initial_indicator_value_2))
        ], className="row", style={
        'textAlign': 'center'
    })

def enhancement(countries_dict):
    """
    Returns the text and image of architecture summary of the project.
    """
    countries = countries_dict.values()
    queries = [cluster.query(country_code) for country_code in countries]
    return html.Div(children=[
        dcc.Markdown('''
            ### Analyzing the Indicators
            Using each indicator as a feature of a country, 
            we can represent a country as a vector of an n-dimensional space (n as in the number of indicators).
            We can then perform principal component analysis to create a visually intuitive clusters of countries.
            This will help us analyze whether the indicators help form groups similar to how they are categorized 
            into developed and developing countries.
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=cluster.clustering(countries, queries)),
    ], className='row', style={
        'textAlign': 'center'
    })

def index():
    return html.Div([
        html.A(html.Button("About"), href='/about', style={'margin': '10px'}),
        html.A(html.Button("Details"), href='/details', style={'margin': '10px'})
    ], style={
        'textAlign': 'center'
    })

def main_page():
    countries_dict = cache['countries']
    indicators_dict = cache['indicators']
    return html.Div([
        title(),
        description(),
        visualization(countries_dict, indicators_dict),
        enhancement(countries_dict),
        index()
    ], style={
        'textAlign': 'center',
    }, className='row', id='content')
