#####################################################################################
# Packages
#####################################################################################
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


#####################################################################################
# Data
#####################################################################################
embedding_df = pd.read_csv('data/dreams_syuzhet_df.csv')
embedding_df = embedding_df.dropna(subset=['content'])
embedding_df = embedding_df.reset_index(drop=True)
embedding_df['text'] = embedding_df['content'].astype(str)
embedding_df['text'] = embedding_df['text'].apply(lambda x: x[:40] + '-<br>' + x[40:80] + '-<br>' + \
                                                            x[80:120] + '...')
embedding_df['text'] = '<b>' + embedding_df['dreamer'] + '</b><br>' + embedding_df['text']

# Prepare Dropdown Levels (Compare)
dreamers_list = embedding_df[['dreamer', 'description']].drop_duplicates()
dreamers_unique = ['All'] + dreamers_list['dreamer'].tolist()
dreamers_desc_unique = ['All Dreamers'] + dreamers_list['description'].tolist()
dreamers_items = [{'label': desc, 'value': dreamer} for dreamer, desc in zip(dreamers_unique, dreamers_desc_unique)]
dreamer_dropdown = dcc.Dropdown(id='dreamer-select', options=dreamers_items, value='All')

# Prepare Dropdown Levels (Compare)
dreamers_unique = ['None'] + dreamers_list['dreamer'].tolist()
dreamers_desc_unique = ['None'] + dreamers_list['description'].tolist()
dreamers_items = [{'label': desc, 'value': dreamer} for dreamer, desc in zip(dreamers_unique, dreamers_desc_unique)]
dreamer_dropdown_comparison = dcc.Dropdown(id='dreamer-compare', options=dreamers_items, value='None')

# Prepare Dropdown Levels (Main)
emotions_list = ['None', 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
dreamers_items = [{'label': el, 'value': el} for el in emotions_list]
dreamer_dropdown_emotions = dcc.Dropdown(id='main-emotion', options=dreamers_items, value='None')


#####################################################################################
# Layouts
#####################################################################################
main_view = html.Div([
    dbc.Row([
        dbc.Col(children=html.H3('All Dreams'), width=12),
    ], justify='center'),

    dbc.Row([
        dbc.Col(children=dreamer_dropdown_emotions, width=4)
    ], justify='center'),

    dbc.Row([dcc.Markdown('')]),

    html.Br(), html.Br(),

    dbc.Card([

        dbc.Row(children=[
            dbc.Col(children=dcc.Graph(id='all-dreams-container'), width=6),
            dbc.Col(children=[
                dcc.Markdown(id='all-dreams-text-container-1', style={"white-space": "pre"}),
                dcc.Markdown(id='all-dreams-text-container-2', style={"overflow-y": "scroll", 'max-height': '300px'})
            ], width=6)
        ])], body=True, style={"border": "1px grey solid"}, color="dark", inverse=True),

    html.Br(), html.Br(),

    dbc.Row([
        dbc.Col(children=html.H3('Word Frequency'), width=6),
        dbc.Col(children=html.H3('Mean Emotional Lexicon'), width=6)
    ]),

    dbc.Row([
        dbc.Col(children=dcc.Graph(id='tfidf-score-container'), width=6),
        dbc.Col(children=dcc.Graph(id='radar-container'), width=6)
    ])
])


compare_view = html.Div([
    # Dreamer Choice
    dbc.Row([
        dbc.Col(children=html.H3('Dreamer'), width=6),
        dbc.Col(children=html.H3(''), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Markdown('**Select a dreamer for display:**'), width=4),
        dbc.Col(dcc.Markdown('**Select a dreamer for comparison:**'), width=4)
    ], justify='between'),
    dbc.Row([
        dbc.Col(dreamer_dropdown, width=4),
        dbc.Col(dreamer_dropdown_comparison, width=4),
    ], justify='between'),

    html.Br(), html.Br(),

    dbc.Row([
        dbc.Col(id='main_dreamer_count', width=4),
        dbc.Col(id='compare_dreamer_count', width=4)
    ], justify='between'),

    html.Br(),


    # Upper Figures
    dbc.Card([
        dbc.Row([
            dbc.Col(children=html.H3('Embedding Visualization'), width=6),
            dbc.Col(children=html.H3(''), width=6)
        ]),

        dbc.Row([
            dbc.Col(children=dcc.Graph(id='embedding-container'), width=6),
            dbc.Col(children=[
                dcc.Markdown(id='text-container-1', style={"white-space": "pre"}),
                dcc.Markdown(id='text-container-2', style={"overflow-y": "scroll", 'max-height': '300px'})
            ], width=6)
        ])
    ], body=True, style={"border": "1px grey solid"}, color="dark", inverse=True),

    html.Br(), html.Br(),


    # Lower Figures
    dbc.Row([
        dbc.Col(children=html.H3('Word Frequency'), width=6),
        dbc.Col(children=html.H3('Mean Emotional Lexicon'), width=6)
    ]),

    dbc.Row([
        dbc.Col(children=dcc.Graph(id='tfidf-container'), width=6),
        dbc.Col(children=dcc.Graph(id='emotion-container'), width=6)
    ])

])



