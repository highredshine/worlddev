import dash_html_components as html
import pandas as pds
from google.oauth2 import service_account
from random import randint

def credentials():
    credentials = service_account.Credentials.from_service_account_file(
        'key.json',
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return credentials

def title():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H1('World Development Indicators')])
    ], className="row", style={
        'textAlign': 'center', 'paddingTop': '3%'
    })

def rand_color():
    c1 = randint(0, 255)
    c2 = randint(0, 255)
    c3 = randint(0, 255)
    color = "rgb(%d,%d,%d)" % (c1,c2,c3)
    return color

COLORS = []

def color():
    color = rand_color()
    if len(COLORS) > 1000:
        i = randint(0, len(COLORS))
        color = COLORS[i]
    else:
        while color in COLORS:
            color = rand_color()
        COLORS.append(color)
    return color

def countries():
    sql = """
        SELECT DISTINCT country_code, short_name as country_name
        FROM `worlddev.wdi.countries`
        ORDER BY country_name
    """
    df = pds.read_gbq(sql, project_id='worlddev', credentials=credentials())
    countries = dict(zip(df.country_name, df.country_code))
    return countries

def indicators():
    sql = """
        SELECT DISTINCT series_code as indicator_code, indicator as indicator_name
        FROM `worlddev.wdi.indicators`
        ORDER BY indicator_name
    """
    df = pds.read_gbq(sql, project_id='worlddev', credentials=credentials())
    indicators = dict(zip(df.indicator_name, df.indicator_code))
    return indicators

countries = countries()
indicators = indicators()
cache = {'countries':countries, 'indicators':indicators}