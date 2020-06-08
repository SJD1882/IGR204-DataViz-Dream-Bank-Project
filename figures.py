#####################################################################################
# Packages
#####################################################################################
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from sklearn.feature_extraction.text import TfidfVectorizer


#####################################################################################
# Figures
#####################################################################################
def get_embedding_scatterplots(embeddings, sizes, opacity_states, colors):
    """ AAA
    """
    data = []
    for embedding, size, opacity, color in zip(embeddings, sizes, opacity_states, colors):
        temp_data = go.Scattergl(x=embedding['Z1'], y=embedding['Z2'], mode='markers',
                                 marker=dict(color=color, size=size, opacity=opacity), hoverinfo='text',
                                 hovertext=embedding['text'], customdata=embedding.index.tolist())
        data.append(temp_data)

    layout = go.Layout(xaxis=dict(showticklabels=False, ticks=''),
                       yaxis=dict(showticklabels=False, ticks=''), margin=dict(t=30),
                       paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgb(245,245,245)',
                       clickmode='event+select', showlegend=False)

    fig = go.Figure(data=data, layout=layout)
    return fig


def get_tfidf_figure(clean_corpus):
    """ AAA
    """
    tfv = TfidfVectorizer(min_df=0, max_features=20, strip_accents='unicode', analyzer='word',
                          ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words='english')

    tfv.fit(clean_corpus)
    features = np.array(tfv.get_feature_names())
    train_grams = tfv.transform(clean_corpus)
    train_grams = pd.DataFrame(train_grams.toarray(), columns=features)
    top_features_all = train_grams.sum(axis=0).sort_values(ascending=False)
    x = top_features_all.index.tolist()
    y = top_features_all.values.tolist()

    # Graph
    data = go.Bar(x=x, y=y, marker_color='grey')
    layout = go.Layout(xaxis=dict(title='Words', tickangle=45), yaxis=dict(title='TFIDF Score'),
                       margin=dict(t=30), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgb(245,245,245)',
                       clickmode='event+select', showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_emoticon_radar_chart():
    """ AAA
    """
    data = go.Scatterpolar(r=[0.25, 0.5, 0.6, 0.75, 0.9, 1.0, 0.05, 0.15],
                           theta=['fear', 'anger', 'trust', 'sadness', 'disgust', 'joy', 'anticip', 'surprise'],
                           fill='toself', line=dict(color='red'))
    layout = go.Layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, margin=dict(t=30),
                       paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgb(245,245,245)')
    fig = go.Figure(data=data, layout=layout)
    return fig

