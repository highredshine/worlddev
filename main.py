import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from common import title
from visuals import callback_byCountries, callback_byIndicator
from cluster import getAllCountries, identify, model, plot

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

def visualization(cache):
    """
    Returns overall project description in markdown
    """
    countries_dict = cache['countries']
    indicators_dict = cache['indicators']
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
        dcc.Graph(id='byIndicator-graph', figure=callback_byIndicator(cache, initial_country_value_1,initial_indicator_value_1)),
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
        dcc.Graph(id='byCountries-graph', figure=callback_byCountries(cache, initial_country_value_2,initial_indicator_value_2))
        ], className="row", style={
        'textAlign': 'center'
    })

def enhancement(cache):
    """
    Returns the text and image of architecture summary of the project.
    """
    countries = getAllCountries(cache)
    initial_clustering = model(countries, cache)
    # first split: developing and developed
    x_vec, _ = initial_clustering
    c1_x = (-1, -0.99)
    c2_x = (0.99, 1)
    developing = identify(countries, x_vec, c1_x)
    developed = identify(countries, x_vec, c2_x)
    developing_clustering = model(developing, cache)
    developed_clustering = model(developed, cache)
    # second split: developing further analysis
    x_vec, _ = developing_clustering
    developing_2nd = identify(developing, x_vec, c1_x)
    developing_3rd = identify(developing, x_vec, c2_x)
    developing_2nd_clustering = model(developing_2nd, cache)
    developing_3rd_clustering = model(developing_3rd, cache)
    # third split: developed further analysis
    x_vec, _ = developed_clustering
    developed_2nd = identify(developed, x_vec, c1_x)
    developed_2nd_cluster = model(developed_2nd, cache)
    # fourth split: developing one more time
    x_vec, _ = developing_2nd_clustering
    developing_4th = identify(developing_2nd, x_vec, c1_x)
    developing_5th = identify(developing_2nd, x_vec, c2_x)
    developing_4th_clustering = model(developing_4th, cache)
    developing_5th_clustering = model(developing_5th, cache)
    return html.Div(children=[
        dcc.Markdown('''
            ### Analyzing the Indicators
            Using each indicator as a feature of a country, 
            we can represent a country as a vector of an n-dimensional space (n as in the number of indicators).
            We can then perform principal component analysis to create a visually intuitive clusters of countries.
            This will help us analyze whether the indicators help form groups similar to how they are categorized 
            into developed and developing countries.
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(countries, initial_clustering)),
        dcc.Markdown('''
            The scatter plot above shows that there are clearly two classifications of the countries, with some outliers.
            Would these two point to developing and developed countries? Let's take a look at the supposedly developed countries.
            #### Developed Countries
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developed, developed_clustering)),
        dcc.Markdown('''
            We can clearly see United States and China (which is actually categorized as developing, but not really).
            But we still see a dense cluster. Let's dig deeper into this one cluster. 
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developed_2nd, developed_2nd_cluster)),
        dcc.Markdown('''
            We surprisingly see a circular distribution. Just like a case for China, we see some large countries that 
            has huge economic and political power in the world arena, but are still categorized as developing. 
            But we can clearly see that the first clustering model categorized major developed countries in the world.
            #### Developing Countries
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developing, developing_clustering)),
        dcc.Markdown('''
            We see some known developing countries, but they are still clustered quite densely.
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developing_3rd, developing_3rd_clustering)),
        dcc.Markdown('''
            We see a good distribution. Interestingly, this cluster seemed to contain a lot of developed countries as well. Why would this be?
            A possible explanation is that the developed countries in this group seem to be small in terms of population.
            Thus, as the clustering is naively done without any consideration of population groups, this result could come out.
            Let's take a look at the second supposingly developing countries.
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developing_2nd, developing_2nd_clustering)),
        dcc.Markdown('''
            We sadly see another two dense clusters. Let's dig deeper.
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developing_4th, developing_4th_clustering)),
        dcc.Markdown('''
            We see some binary classification here again. We can see some similarities between the countries here:
            The first group seems to contain a lot of island countries, and the second group contains a lot of
            countries with rural or undeveloped lands. 
            
        '''),
        dcc.Graph(id='stacked-trend-graph', figure=plot(developing_5th, developing_5th_clustering)),
        dcc.Markdown('''
            The second cluster also seems to be binarlily split. These classifications are vague, but seems to be geographically categorized.
        ''')
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

def main_page(cache):
    return html.Div([
        title(),
        description(),
        visualization(cache),
        enhancement(cache),
        index()
    ], style={
        'textAlign': 'center',
    }, className='row', id='content')
