import pandas as pds
import numpy as np
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from common import credentials, cache

def query(country_code):
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

def clustering(countries, queries):
    pca = PCA(n_components=3)
    embeddings = queries[0].rename(columns={'mean':countries[0]})
    for i in range(1,len(queries)):
        embeddings = pds.merge(embeddings, 
                               queries[i].rename(columns={'mean':countries[i]}), 
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
    countries = ['World', 'China', 'USA', 'Brazil']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = x_vec,
        y = y_vec,
        mode = 'markers+text',
        text = countries,
        textposition='top center'
    ))
    fig.update_layout(template='plotly_dark',
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c'
                      )
    return fig