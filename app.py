#####################################################################################
# Packages
#####################################################################################
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from callbacks import *


#####################################################################################
# Data
#####################################################################################
embedding_df = pd.read_csv('data/dreams_umap_df.csv')
embedding_df = embedding_df.dropna(subset=['content'])
embedding_df = embedding_df.reset_index(drop=True)
embedding_df['text'] = embedding_df['content'].astype(str)
embedding_df['text'] = embedding_df['text'].apply(lambda x: x[:40] + '-<br>' + x[40:80] + '-<br>' + \
                                                            x[80:120] + '...')
embedding_df['text'] = '<b>' + embedding_df['dreamer'] + '</b><br>' + embedding_df['text']
dreamers = embedding_df['dreamer'].unique().tolist()
dreamers = ['All'] + dreamers
dreamers_items = [{'label': el, 'value': el} for el in dreamers]
dreamer_dropdown = dcc.Dropdown(id='dreamer-select', options=dreamers_items,
                                value='All')


#####################################################################################
# Layout
#####################################################################################
layout = dbc.Container([
    # Main Header
    html.Br(),
    html.H1('Decrypting DreamBank'),
    html.Br(), html.Br(),

    # Dreamer Choice
    html.H5('Dreamer'),
    dbc.Row(
        dbc.Col(dreamer_dropdown, width=4)
    ),
    html.Br(), html.Br(),

    # Upper Figures
    dbc.Row([
        dbc.Col(children=html.H3('Dream Embedding Visualization'), width=6),
        dbc.Col(children=html.H3('Dream Viewer'), width=6)
    ]),

    dbc.Row([
        dbc.Col(children=dcc.Graph(id='embedding-container'), width=6),
        dbc.Col(children=[
            dcc.Markdown(id='text-container-1', style={"white-space": "pre"}),
            dcc.Markdown(id='text-container-2', style={"overflow-y": "scroll", 'max-height': '300px'})
        ], width=6)
    ]),

    # Lower Figures
    dbc.Row([
        dbc.Col(children=html.H3('Word Frequency'), width=6),
        dbc.Col(children=html.H3('Emotive Lexicon Analysis'), width=6)
    ]),

    dbc.Row([
        dbc.Col(children=dcc.Graph(id='tfidf-container'), width=6),
        dbc.Col(children=dcc.Graph(id='emotion-container'), width=6)
    ]),

])

external_style_sheets = [dbc.themes.SIMPLEX]
app = dash.Dash(__name__, external_stylesheets=external_style_sheets)
app.config.suppress_callback_exceptions = True
app.layout = layout


#####################################################################################
# Callbacks
#####################################################################################
get_app_callbacks(app, embedding_df)


# Main
if __name__ == '__main__':
    app.run_server(debug=True)


