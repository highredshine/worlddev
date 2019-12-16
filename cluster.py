import pandas as pds
import numpy as np
from sklearn.manifold import TSNE
from sklearn import preprocessing
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from common import credentials

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
    df = pds.read_gbq(sql, configuration=config, project_id='worlddev', credentials=credentials())
    return df

def create_embedding(wld, chn, usa, bra):
    merge1 = pds.merge(wld, chn, on='indicator', how='inner')
    merge1 = merge1.rename(columns={"mean_x": "wld", "mean_y": "chn"})
    merge2 = pds.merge(usa, bra, on='indicator', how='inner')
    merge2 = merge2.rename(columns={"mean_x": "usa", "mean_y": "bra"})
    embeddings = pds.merge(merge1, merge2, on='indicator', how='inner')
    embeddings = embeddings.drop(['indicator'], axis=1)
    embeddings = np.transpose(np.array(embeddings))
    return embeddings

def clustering(embeddings):
    pca = PCA(n_components=2)
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
                      paper_bgcolor='#23272c')
    return fig