#####################################################################################
# Packages
#####################################################################################
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from callbacks import *
from layouts import *


#####################################################################################
# Layout
#####################################################################################
layout = dbc.Container([


    # Main Header
    html.Br(),
    html.H1('Decrypting DreamBank'),
    html.Br(), html.Br(),

    # Tabs
    dbc.CardHeader([
        dbc.Tabs([
            dbc.Tab(label='Dream View', id='tab-0'),
            # dbc.Tab(label='Time Series View', id='tab-1')
        ], id='container_tabs', active_tab='tab-0')
    ]),

    # Displayed Content
    html.Br(), html.Br(),
    html.Div(id='displayed_tab')

])


external_style_sheets = [dbc.themes.CERULEAN]
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


