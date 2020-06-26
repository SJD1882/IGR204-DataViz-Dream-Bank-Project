#####################################################################################
# Packages
#####################################################################################
from dash.dependencies import Input, Output
from figures import *
from layouts import *


#####################################################################################
# Callbacks
#####################################################################################
def get_app_callbacks(app, embedding_df):
    """ AAA
    """
    @app.callback(
        Output('embedding-container', 'figure'),
        [Input('dreamer-select', 'value'),
         Input('dreamer-compare', 'value')]
    )
    def create_umap_graph(dreamer, compare):
        """ AAA
        """
        embedding = embedding_df.copy()

        if (dreamer == 'All'):
            embbedings = [embedding]
            fig = get_embedding_scatterplots(embbedings, [2], [1.0], ['darkblue'], names=['All'])

        elif (dreamer != 'All') and (compare == 'None'):
            # Prepare data
            embedding_selected = embedding_df[embedding_df['dreamer'] == dreamer].copy()
            embedding_others = embedding_df[embedding_df['dreamer'] != dreamer].copy()
            embbedings = [embedding_others, embedding_selected]

            # Scatter plot
            fig = get_embedding_scatterplots(embbedings, sizes=[2, 5], opacity_states=[0.35, 1.0],
                                             colors=['grey', 'darkblue'], names=['All', dreamer])

        elif (dreamer != 'All') and (compare != 'None'):
            # Prepare data
            embedding_selected = embedding_df[embedding_df['dreamer'] == dreamer].copy()
            embedding_compare = embedding_df[embedding_df['dreamer'] == compare].copy()
            embedding_others = embedding_df[~embedding_df['dreamer'].isin([dreamer, compare])].copy()
            embbedings = [embedding_others, embedding_selected, embedding_compare]

            # Scatter plot
            fig = get_embedding_scatterplots(embbedings, sizes=[2, 5, 5], opacity_states=[0.35, 1.0, 1.0],
                                             colors=['grey', 'darkblue', 'red'], names=['All', dreamer, compare])

        return fig


    @app.callback(
        Output('tfidf-container', 'figure'),
        [Input('dreamer-select', 'value'),
         Input('dreamer-compare', 'value')]
    )
    def create_tfidf_score(dreamer, compare):
        """ AAA
        """
        embedding = embedding_df.copy()

        if (dreamer == 'All'):
            # Unigrams and Bigrams
            clean_corpus = embedding['text_cleaned'].values
            fig = get_tfidf_figure([clean_corpus], colors=['darkblue'], names=['All'])

        elif (dreamer != 'All') and (compare == 'None'):
            # Prepare data
            embedding_selected = embedding[embedding['dreamer'] == dreamer]
            clean_corpus = embedding_selected['text_cleaned'].values
            fig = get_tfidf_figure([clean_corpus], colors=['darkblue'], names=[dreamer])

        elif (dreamer != 'All') and (compare != 'None'):
            # Prepare data
            embedding_selected = embedding[embedding['dreamer'] == dreamer]
            embedding_compare = embedding[embedding['dreamer'] == compare]

            clean_corpus_selected = embedding_selected['text_cleaned'].values
            clean_corpus_compare = embedding_compare['text_cleaned'].values

            fig = get_tfidf_figure([clean_corpus_selected, clean_corpus_compare],
                                   colors=['darkblue', 'red'], names=[dreamer, compare])

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

        dream = embedding_df['content'].iloc[dream_idx]
        date = embedding_df['date'].iloc[dream_idx]
        author = embedding_df['description'].iloc[dream_idx]
        title = 'Dreamer: **{}**\nDate: {}\nTranscript:'.format(author, date)
        text = '{}'.format(dream)
        return title, text


    @app.callback(
        Output('emotion-container', 'figure'),
        [Input('dreamer-select', 'value'),
         Input('dreamer-compare', 'value')]
    )
    def get_emotion_scores(dreamer, compare):
        """ AAA
        """
        emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
        embedding = embedding_df.copy()

        if (dreamer == 'All'):
            mean_scores = [embedding[emotions].mean()]
            fig = get_emoticon_radar_chart(mean_scores, ['darkblue'], ['All'])

        elif (dreamer != 'All') and (compare == 'None'):
            embedding_1 = embedding_df[embedding_df['dreamer'] == dreamer].copy()
            mean_scores_1 = embedding_1[emotions].mean()
            scores = [mean_scores_1]
            fig = get_emoticon_radar_chart(scores, ['darkblue', 'red'], [dreamer, compare])

        elif (dreamer != 'All') and (compare != 'None'):
            embedding_1 = embedding_df[embedding_df['dreamer'] == dreamer].copy()
            embedding_2 = embedding_df[embedding_df['dreamer'] == compare].copy()
            mean_scores_1 = embedding_1[emotions].mean()
            mean_scores_2 = embedding_2[emotions].mean()
            scores = [mean_scores_1, mean_scores_2]
            fig = get_emoticon_radar_chart(scores, ['darkblue', 'red'], [dreamer, compare])

        return fig


    @app.callback(
        [Output('main_dreamer_count', 'children'),
         Output('compare_dreamer_count', 'children')],
        [Input('dreamer-select', 'value'),
         Input('dreamer-compare', 'value')]
    )
    def update_count(dreamer, compare):
        """ AAA
        """
        embedding = embedding_df.copy()

        if (dreamer == 'All'):
            nb_count_dreamer = len(embedding)
            text_dreamer = dcc.Markdown("**Dream Count**:  {}".format(nb_count_dreamer))
            compare_dreamer = dcc.Markdown("")

        elif (dreamer != 'All') and (compare == 'None'):
            nb_count_dreamer = embedding[embedding['dreamer'] == dreamer].shape[0]
            text_dreamer = dcc.Markdown("**Dream Count**:  {}".format(nb_count_dreamer))
            compare_dreamer = dcc.Markdown("")

        elif (dreamer != 'All') and (compare != 'None'):
            nb_count_dreamer = embedding[embedding['dreamer'] == dreamer].shape[0]
            nb_count_compare = embedding[embedding['dreamer'] == compare].shape[0]
            text_dreamer = dcc.Markdown("**Dream Count**:  {}".format(nb_count_dreamer))
            compare_dreamer = dcc.Markdown("**Dream Count**:  {}".format(nb_count_compare))

        return text_dreamer, compare_dreamer


    @app.callback(
        Output('displayed_tab', 'children'),
        [Input('container_tabs', 'active_tab')]
    )
    def change_tab(tab_name):
        """ AAA
        """
        if tab_name == 'tab-0':
            return main_view
        elif tab_name == 'tab-1':
            return compare_view
        return 'Loading...'


    @app.callback(
        Output('all-dreams-container', 'figure'),
        [Input('main-emotion', 'value')]
    )
    def get_figure(main_emotion):
        """ AAA
        """
        embedding = embedding_df.copy()

        if main_emotion == 'None':
            embeddings = [embedding]
            fig = get_embedding_scatterplots(embeddings, [2], [1.0], ['darkblue'], names=['All'])
        else:
            emotion = embedding[main_emotion].copy()
            fig = get_scatterplot_with_emotions(embedding, emotion, main_emotion)

        return fig



    @app.callback(
        [Output('tfidf-score-container', 'figure'),
         Output('radar-container', 'figure')],
        [Input('all-dreams-container', 'selectedData')]
    )
    def get_figure(dream_list):
        """ AAA
        """
        emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']

        if dream_list is not None:
            dream_list = [el['customdata'] for el in dream_list['points']]
            selected_data = embedding_df.iloc[dream_list]
            clean_corpus = selected_data['text_cleaned'].copy()
            mean_scores = [selected_data[emotions].mean()]

            # Get Figures
            fig_tfidf_scores = get_tfidf_figure([clean_corpus], colors=['darkblue'], names=['All'])
            fig_radar_plot = get_emoticon_radar_chart(mean_scores, ['darkblue'], ['All'])

        else:
            clean_corpus = embedding_df['text_cleaned'].copy()
            mean_scores = [embedding_df[emotions].mean()]

            # Get Figures
            fig_tfidf_scores = get_tfidf_figure([clean_corpus], colors=['darkblue'], names=['All'])
            fig_radar_plot = get_emoticon_radar_chart(mean_scores, ['darkblue'], ['All'])

        return fig_tfidf_scores, fig_radar_plot

