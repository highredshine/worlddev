import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from common import title
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

def visualization():
    """
    Returns overall project description in markdown
    """
    country_code = 'WLD'
    indicator = 'Access to clean fuels and technologies for cooking'
    df = visuals.query(country_code, indicator)
    return html.Div(children=[
        dcc.Markdown('''
            ### Observing the Indicators
            The data consists all the annual time series data of numerous indicators 
            gathered from all around the world. The default plot shows the world average of some of the
            representative indicators such as electricity access. There are several ways to oberse the data.
            ###### - choose one country and pick one or more indicators to understand the development of the country.
            ###### - choose one indicator and pick one or more countries to understand the relevance of the indicator.
        '''),
        # TODO: visualization
        dcc.Graph(id='stacked-trend-graph', figure=visuals.visualize(df, stack=True)),
        ], className="row", style={
        'textAlign': 'center'
    })

def enhancement():
    """
    Returns the text and image of architecture summary of the project.
    """
    wld = cluster.query('WLD')
    chn = cluster.query('CHN')
    usa = cluster.query('USA')
    bra = cluster.query('BRA')
    embeddings = cluster.create_embedding(wld, chn, usa, bra)
    return html.Div(children=[
        dcc.Markdown('''
            ### Analyzing the Indicators
            Using each indicator as a feature of a country, 
            we can represent a country as a vector of an n-dimensional space (n as in the number of indicators).
            Using these vectors, we can cluster the country vectors, and analyze whether they form groups similar
            to how they are categorized into developed and developing countries. We can visualize these clusters
            with either the average values of the indicators, or by each year. This way, we can see if the
            clusters (development status) change as time passed.
        '''),
        # TODO: clusters
        dcc.Graph(id='stacked-trend-graph', figure=cluster.clustering(embeddings)),
        dcc.Markdown('''
            The dataset also has categorized all countries into 'income_group.' We can use this data as labels
            for predicting which indicators can most accurately categorize a country to its current development status.
            This will tell us which indicators are the most relevant to development. The following is a visualization
            of the knn model.
        '''),
        # TODO: knn model
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
    return html.Div([
        title(),
        description(),
        visualization(),
        enhancement(),
        index()
    ], style={
        'textAlign': 'center',
    }, className='row', id='content')
