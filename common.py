import dash_html_components as html
from google.oauth2 import service_account
import requests

def credentials():
    credentials = service_account.Credentials.from_service_account_file(
        'key.json',
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return credentials

def address():
    response = requests.get('https://compute.googleapis.com/compute/v1/projects/worlddev/zones/us-central1-a/instances/webapp')
    addr = response['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    return addr

def title():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H1('World Development Indicators')])
    ], className="row", style={
        'textAlign': 'center', 'paddingTop': '3%'
    })