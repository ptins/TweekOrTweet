import numpy as np
import pandas as pd
# from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

## start app

app = dash.Dash(__name__)
server = app.server

df_people = pd.read_csv('people_list.csv')

### FROM DF ###

df_from = pd.read_csv('user_tweets_from.csv')
df_about = pd.read_csv('user_tweets_about.csv')

# df_from['daysSince'] = datetime.utcnow() - pd.to_datetime(df_from['created_at'])
# df_about['daysSince'] = datetime.utcnow() - pd.to_datetime(df_about['created_at'])

# print(df_from.head())
# print(df_about.head())

df_from = pd.merge(left=df_from, right=df_people)
#
# ## feature engineering
df_from['rfr'] = (1.0*df_from['favorite_count']+1.0*df_from['retweet_count'])/df_from['followers_count']
#
# ## normalize
df_from['favorite_count_norm'] = df_from['favorite_count'] / df_from['favorite_count'].max()
df_from['retweet_count_norm']  = df_from['retweet_count'] / df_from['retweet_count'].max()
df_from['followers_count_norm'] = df_from['followers_count'] / df_from['followers_count'].max()
df_from['rfr_norm'] = df_from['rfr'] / df_from['rfr'].max()

## separate
celeb_df_from = df_from[df_from['industry'] == 'celebrity']
athlete_df_from = df_from[df_from['industry'] == 'athlete']
musician_df_from = df_from[df_from['industry'] == 'musician']

### END FROM DF ###

### ABOUT DF ###

# df_about = pd.read_csv('user_tweets_about.csv', header=None)
# df_about.columns = ['tweet_id','created_at','favorite_count','retweet_count','text',
#             'polarity','screen_name','industry']
#
# df_about = pd.merge(left=df_about, right=df_people)
#
# df_about['polarity'] = df_about['polarity']+1
#
# celeb_df_about = df_about[df_about['industry'] == 'celebrity']
# athlete_df_about = df_about[df_about['industry'] == 'athlete']
# musician_df_about = df_about[df_about['industry'] == 'musician']

### END ABOUT DF ###

# trace1 = dict(
#         type='scatterternary',
#         a = df_from['retweet_count_norm'],
#         b = df_from['rfr_norm'],
#         c = df_from['favorite_count_norm'],
#         text = df_from['text'],
#         mode = 'markers',
#         opacity = .5,
#         marker = {
#             'symbol': 'x',
#             'color': 'red',
#             'size': 10
#         },
#         name = 'Controversial'
# )

app.layout = html.Div(children=[

    # Title Stuff
    html.Div(children=[
        html.H1(
            children='Twitter Persona Likability'),
        html.H4(
            children='Judging Individuals\' Likability Based on Tweeting Habits'),
        html.Hr(style={'width':'400'}),
        ],
        style={
            'text-align': 'center'
        },
        className='twelve columns',
    ),

    # Left Half (Dropdowns and Graph)
    html.Div(children=[
        # Dropdowns
        html.Label('Select Industry (>1 Allowed):'),
        dcc.Dropdown(
        options=[
            {'label': 'Athletes', 'value': 'Athletes'},
            {'label': 'Celebrities', 'value': 'Celebrities'},
            {'label': 'Musicians', 'value': 'Musicians'}
        ],
        value=['Athletes'],
        multi=True
        ),
    ], style='six columns')

    # dcc.Graph(
    #     id = 'celeb-ind',
    #     style = {
    #             'width': '50%',
    #             'display': 'inline-block'
    #     },
    #     figure = {
    #         'data': [trace1],
    #         'layout': {
    #             'ternary': {
    #                 'sum': 1,
    #                 'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
    #                 'baxis': {'title': 'RFR', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
    #                 'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
    #             },
    #             'annotations': [{
    #                 'showarrow': False,
    #                 'text': 'Individual Tweets',
    #                 'x': 0.5,
    #                 'y': 1.3,
    #                 'font': { 'size': 25 }
    #             }]
    #         }
    #     }
    # ),

])

if __name__ == '__main__':
    app.run_server(debug=False)
