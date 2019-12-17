import pandas as pds
import numpy as np
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from common import credentials

def query(cache, country_code):
    sql = """
        SELECT indicator, AVG(value) as mean
        FROM `worlddev.wdi.main`
        WHERE country_code = @country_code
        GROUP BY indicator
    """
    config = {
        'query': {
            'parameterMode': 'NAMED',
            'queryParameters': [
                {
                    'name': 'country_code',
                    'parameterType': {'type': 'STRING'},
                    'parameterValue': {'value': country_code}
                }
            ]
        }
    }
    if country_code not in cache:
        cache[country_code] = pds.read_gbq(sql, 
                                           configuration=config, 
                                           project_id='worlddev', 
                                           credentials=credentials())
    return cache[country_code]

def getAllCountries(cache):
    sql = """
        SELECT m.country_code, country_name
        FROM `worlddev.wdi.main` as m, `worlddev.wdi.countries` as c
        WHERE m.country_code = c.country_code
        GROUP BY country_code, country_name
        HAVING COUNT(DISTINCT m.indicator)>= 249
    """
    if 'all' not in cache:
        cache['all'] = pds.read_gbq(sql, 
                                           project_id='worlddev', 
                                           credentials=credentials())
    countries = cache['all']
    return countries

def getIndicators(countries, cache):
    queries = []
    for country_code in countries['country_code']:
        queries.append(query(cache, country_code))
    return queries

def between(vec, xrange):
    indices = []
    a, b = xrange
    for i in range(len(vec)):
        val = vec[i]
        if val > a and val < b:
            indices.append(i)
    return indices

def identify(countries, vec, cluster_range):
    codes = np.array(countries['country_code'])
    names = np.array(countries['country_name'])
    codes_c = codes[between(vec, cluster_range)]
    names_c = names[between(vec, cluster_range)]
    cluster = pds.DataFrame({'country_code': codes_c, 'country_name': names_c}, 
                            columns=['country_code', 'country_name'])
    return cluster

def model(countries, cache):
    pca = PCA(n_components=2)
    queries = getIndicators(countries, cache)
    embeddings = queries[0].rename(columns={'mean':countries['country_code'][0]})
    for i in range(1,len(queries)):
        embeddings = pds.merge(embeddings, 
                               queries[i].rename(
                                   columns={'mean':countries['country_code'][i]}), 
                               on='indicator', how='inner')
    embeddings = embeddings.drop(['indicator'], axis=1)
    embeddings = np.transpose(np.array(embeddings))
    vectors = pca.fit_transform(embeddings)
    normalizer = preprocessing.Normalizer()
    norm_vectors = normalizer.fit_transform(vectors, 'l2')
    x_vec = []
    y_vec = []
    for x,y in norm_vectors:
        x_vec.append(x)
        y_vec.append(y)
    return x_vec, y_vec
        
def plot(countries, coordinates):
    x_vec, y_vec = coordinates
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = x_vec,
        y = y_vec,
        mode = 'markers+text',
        text = countries['country_name'],
        textposition='top center'
    ))
    fig.update_layout(template='plotly_dark',
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c'
                      )
    return fig