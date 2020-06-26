#####################################################################################
# Packages
#####################################################################################
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.feature_extraction.text import TfidfVectorizer


#####################################################################################
# Figures
#####################################################################################
def get_embedding_scatterplots(embeddings, sizes, opacity_states, colors, names):
    """ AAA
    """
    data = []
    for embedding, size, opacity, color, name in zip(embeddings, sizes, opacity_states, colors, names):
        temp_data = go.Scattergl(x=embedding['Z1'], y=embedding['Z2'], mode='markers',
                                 marker=dict(color=color, size=size, opacity=opacity), hoverinfo='text',
                                 hovertext=embedding['text'], customdata=embedding.index.tolist(),
                                 name=name)
        data.append(temp_data)

    layout = go.Layout(xaxis=dict(showticklabels=False, ticks=''), yaxis=dict(showticklabels=False, ticks=''),
                       margin=dict(t=30), paper_bgcolor='rgba(0,0,0,0)', clickmode='event+select', showlegend=True,
                       legend=dict(font=dict(color="white")), legend_orientation="h")

    fig = go.Figure(data=data, layout=layout)
    return fig


def get_tfidf_scores(clean_corpus):
    """ AAA
    """
    tfv = TfidfVectorizer(min_df=0, max_features=15, strip_accents='unicode', analyzer='word',
                          ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words='english')

    tfv.fit(clean_corpus)
    features = np.array(tfv.get_feature_names())
    train_grams = tfv.transform(clean_corpus)
    train_grams = pd.DataFrame(train_grams.toarray(), columns=features)
    top_features_all = train_grams.sum(axis=0).sort_values(ascending=False)
    return top_features_all


def get_tfidf_figure(cleaned_corpus_list, colors, names):
    """ AAA
    """
    # Get TFIDF scores
    tfidf_scores = []
    for corpus in cleaned_corpus_list:
        tfidf_score = get_tfidf_scores(corpus)
        tfidf_scores.append(tfidf_score)

    # Graph
    fig = make_subplots(rows=2, cols=1)

    data = []
    i = 0
    for tfidf_score, color, name in zip(tfidf_scores, colors, names):
        i += 1
        x = tfidf_score.index
        y = tfidf_score.values
        temp_data = go.Bar(x=x, y=y, marker_color=color, name=name)
        fig.append_trace(temp_data, row=i, col=1)
        fig.update_xaxes(tickangle=45, row=i, col=1)
        fig.update_yaxes(title_text="TFIDF Score", row=i, col=1)

    fig.update_layout(margin=dict(t=30), paper_bgcolor='rgba(0,0,0,0)', clickmode='event+select',
                      showlegend=True, xaxis=dict(tickangle=45))

    return fig



def get_emoticon_radar_chart(scores_list, colors, names):
    """ AAA
    """
    data_radars = []
    emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
    for score, color, name in zip(scores_list, colors, names):
        data = go.Scatterpolar(r=score, theta=emotions, fill='toself', line=dict(color=color), name=name)
        data_radars.append(data)

    layout = go.Layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, margin=dict(t=30),
                       paper_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=data_radars, layout=layout)

    return fig


def get_scatterplot_with_emotions(embedding, emotion, emotion_name):
    """ AAA
    """
    fig = go.Figure()

    colorbar_dict = dict(thickness=20, tickmode='array', titleside='right',
                         title=dict(text=emotion_name + ' (Nb. of words related to)',
                                    font=dict(size=13, color='white')),
                         outlinecolor='black', outlinewidth=1, tickfont=dict(color='white'))
    # hover_text = [''.format(score) for score in emotion]
    marker_dict = dict(color=emotion,
                       size=5, opacity=0.75, colorscale='Reds', colorbar=colorbar_dict)

    fig.add_trace(
        go.Scattergl(x=embedding['Z1'], y=embedding['Z2'], mode='markers',
                     marker=marker_dict, hovertext=embedding['text'], customdata=embedding.index.tolist(),
                     hoverinfo='text')
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showticklabels=False, ticks=''),
        yaxis=dict(showticklabels=False, ticks=''), margin=dict(t=30), legend=dict(font=dict(color="white"))
    )

    return fig



