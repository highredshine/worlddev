import dash
import dash_core_components as dcc
import dash_html_components as html
from common import title


def index():
    return html.Div([
        html.A(html.Button("Home"), href='/', style={'margin': '10px'}),
        html.A(html.Button("Details"), href='/details', style={'margin': '10px'})
    ], style={
        'textAlign': 'center'
    })

def page_header():
    return html.Div([
        html.H3('About')
    ], style={
        'textAlign': 'center'
    })

def content():
    return html.Div(children=[
        dcc.Markdown('''
            #### Summary
            As explained in the main page, Jared Diamon discusses in this book Guns, Germs, and Steel how 
            some countries could become extremely developed while some could not. What if we can approach
            this idea in a data scientific way? What if we can analyze the past and present data on 
            various characteristics of the countries, and use machine learning techniques to understand
            what led to the current status of countries?
            #### Dataset
            This project is based on World Bank's dataset called World Development Indicators. An indicator
            is a thematic item, like access to electricity, GDP per capita, CO2 emission, gender equality,
            and etc. These data has been collected throughout the 20th century and to the latest year, for all
            countries. For further information about how the dataset looks, go to Details page.
            #### Performance
            The analysis led to a conclusion that baseline model is unnecessary. The number of features as well
            as the number of neighbors for the KNN model completely depended on the countriesand the types of 
            indicators used in the model. 
            #### Next Steps
            There are some studies to capture the time series pattern as another feature for this kind of analysis.
            It may be valuable to incorporate such concepts into clustering and modeling efforts.
            #### References
            
        ''', className='eleven columns', 
        style={'paddingLeft': '5%'})
    ], className="row", id='about-content'
    )

about_page = html.Div([
    title(),
    page_header(),
    content(),
    index()
])
