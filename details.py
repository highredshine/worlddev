import dash
import dash_core_components as dcc
import dash_html_components as html
from common import title

def index():
    return html.Div([
        html.A(html.Button("Home"), href='/', style={'margin': '10px'}),
        html.A(html.Button("About"), href='/about', style={'margin': '10px'})
    ], style={
        'textAlign': 'center'
    })

def page_header():
    return html.Div([
        html.H3('Details')
    ], style={
        'textAlign': 'center'
    })

def content1(app):
    return html.Div(children=[
        dcc.Markdown('''
            #### Development Process
            The front-end developemnt was through Dash, a Python framework for building web applications.
            As the platform was on Dash, it was suitable to use Plotly framework for any visauzliation works.

            #### Technology Stack
            The data was stored in Google Cloud Platform's BigQuery. World Bank's WDI dataset is public and
            has been already uploaded to BigQuery's public dataset platform. 

            #### Data Acquisition
            As the website is built on Dash, a Python framework, the data was also retrieved and stored
            as Python's Pandas dataframe. Pandas could be directly connected to BigQuery's API. Using already
            saved and parametrized SQL queries, the application retrieves the data and stores it as pandas dataframe.
            The caching process was convenient as BigQuery automatically caches the queries.

            #### ETL (Extract, Transform, Load)
            The original dataset from World Bank consists of six tables:
            ###### - country_series_definitions: contains country and indicator IDs.
            ###### - country_summary: latest update on country specific information.
            ###### - indicator_data: main time series data
            ###### - series_summary: table for each indicator and its specific details
            ###### - series_time: specific information about the indicator at each year.
            ###### - footnotes
            The project used data from country_summary, indicator_data, and series_summary.
            Using these datasets, the GCP client builds three tables:
            ###### - countries: filtered countries with only relevant information.
            ###### - indicators: filtered indicators based on topics and redundancy.
            ###### - main: an updated indicator_data with only the indicators selected.
            Both country_summary and indicator_data updates periodically whenever a new data comes in. The project's
            BigQuery client constantly updates the countries and main tables based on these insertions.

            #### Database Design
            ''', 
            className='eleven columns', 
            style={'paddingLeft': '5%'}
        ),
        html.Div(children=[
            html.Img(src=app.get_asset_url('schema.png'),
                className='row',
                style={'width':'80%', 'height':'80%'}),
            ], 
            className='row', 
            style={'textAlign': 'center'}
        ),
    ], className="row", id='about-content'
    )
    
def content2():
    return html.Div(children=[
        dcc.Markdown('''
            #### EDA (Exploratory Data Analysis)
            https://github.com/juatho/worlddev/blob/master/ETL_EDA.ipynb
            #### Enhancement
            https://github.com/juatho/worlddev/blob/master/Enhancement.ipynb
            ''', 
            className='eleven columns', 
            style={'paddingLeft': '5%'}
        )
    ], className="row", id='about-content'
    )

def details_page(app):
    return html.Div([
        title(),
        page_header(),
        content1(app),
        content2(),
        index()
    ])
