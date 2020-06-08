#####################################################################################
# Packages
#####################################################################################
from dash.dependencies import Input, Output
from figures import *


#####################################################################################
# Callbacks
#####################################################################################
def get_app_callbacks(app, embedding_df):
    """ AAA
    """
    @app.callback(
        Output('embedding-container', 'figure'),
        [Input('dreamer-select', 'value')]
    )
    def create_umap_graph(dreamer):
        """ AAA
        """
        embedding = embedding_df.copy()

        if dreamer == 'All':
            embbedings = [embedding]
            fig = get_embedding_scatterplots(embbedings, [2], [1.0], ['grey'])

        else:
            # Prepare data
            embedding_selected = embedding_df[embedding_df['dreamer'] == dreamer]
            embedding_others = embedding_df[embedding_df['dreamer'] != dreamer]
            embbedings = [embedding_others, embedding_selected]

            # Scatter plot
            fig = get_embedding_scatterplots(embbedings, sizes=[2, 5], opacity_states=[0.35, 1.0],
                                             colors=['grey', 'red'])

        return fig


    @app.callback(
        Output('tfidf-container', 'figure'),
        [Input('dreamer-select', 'value')]
    )
    def create_tfidf_score(dreamer):
        """ AAA
        """
        embedding = embedding_df.copy()

        if dreamer == 'All':
            # Unigrams and Bigrams
            clean_corpus = embedding_df['text_cleaned'].values
            fig = get_tfidf_figure(clean_corpus)

        else:
            # Prepare data
            embedding_selected = embedding_df[embedding_df['dreamer'] == dreamer]
            clean_corpus = embedding_selected['text_cleaned'].values
            fig = get_tfidf_figure(clean_corpus)

        return fig


    @app.callback(
        [Output('text-container-1', 'children'),
         Output('text-container-2', 'children')],
        [Input('embedding-container', 'clickData')]
    )
    def get_dream_view(clicked_dream):
        if clicked_dream is not None:
            dream_idx = clicked_dream['points'][0]['customdata']
        else:
            dream_idx = 0

        print(clicked_dream)

        dream = embedding_df['content'].iloc[dream_idx]
        date = embedding_df['date'].iloc[dream_idx]
        author = embedding_df['description'].iloc[dream_idx]
        title = 'Dreamer: **{}**\nDate: {}\nTranscript:'.format(author, date)
        text = '{}'.format(dream)
        return title, text


    @app.callback(
        Output('emotion-container', 'figure'),
        [Input('dreamer-select', 'value')]
    )
    def create_tfidf_score(dreamer):
        """ AAA
        """
        embedding = embedding_df.copy()

        if dreamer == 'All':
            fig = get_emoticon_radar_chart()

        else:
            embedding_selected = embedding_df[embedding_df['dreamer'] == dreamer]
            fig = get_emoticon_radar_chart()

        return fig

