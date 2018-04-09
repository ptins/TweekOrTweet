import numpy as np
import pandas as pd

from sklearn import preprocessing

import dash
import dash_core_components as dcc
import dash_html_components as html

## start app

app = dash.Dash(__name__)
server = app.server

## load data

df = pd.read_csv('user_tweets_from.csv', header=None)
df.columns = ['tweet_id','created_at','text',
            'favorite_count','retweet_count','followers_count',
            'screen_name','industry']

# feature engineering
df['rfr'] = (df['favorite_count']+df['retweet_count'])/df['followers_count']

# normalize
df['favorite_count_norm'] = df['favorite_count'] / df['favorite_count'].max()
df['retweet_count_norm']  = df['retweet_count'] / df['retweet_count'].max()
df['followers_count_norm'] = df['followers_count'] / df['followers_count'].max()
df['rfr_norm'] = df['rfr'] / df['rfr'].max()

# separate
celeb_df = df[df['industry'] == 'celebrity']
athlete_df = df[df['industry'] == 'athlete']
musician_df = df[df['industry'] == 'musician']

df_ave = df.groupby('screen_name').mean()

people = pd.read_csv('people_list.csv')

df_ave = pd.merge(left=df_ave, right=people, left_index=True, right_on='screen_name').drop('tweet_id', axis=1)
# print(df_ave.head())

celeb_df_ave = df_ave[df_ave['industry'] == 'celebrity']
athlete_df_ave = df_ave[df_ave['industry'] == 'athlete']
musician_df_ave = df_ave[df_ave['industry'] == 'musician']

trace1 = dict(
        type='scatterternary',
        a = celeb_df['retweet_count_norm'],
        b = celeb_df['rfr_norm'],
        c = celeb_df['favorite_count_norm'],
        text = celeb_df['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 10
        },
        name = 'celebrity'
)

trace2 = dict(
        type = 'scatterternary',
        a = athlete_df['retweet_count_norm'],
        b = athlete_df['rfr_norm'],
        c = athlete_df['favorite_count_norm'],
        text = athlete_df['screen_name'],
        mode ='markers',
        opacity = .5,
        marker = {
            'symbol': athlete_df['screen_name'],
            'color': 'red',
            'size': 10
        },
        name = 'athlete'
)

trace3 = dict(
        type = 'scatterternary',
        a = musician_df['retweet_count_norm'],
        b = musician_df['rfr_norm'],
        c = musician_df['favorite_count_norm'],
        text = musician_df['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': musician_df['screen_name'],
            'color': 'blue',
            'size': 10
        },
        name = 'musician'
)

trace4 = dict(
        type='scatterternary',
        a = celeb_df_ave['retweet_count_norm'],
        b = celeb_df_ave['rfr_norm'],
        c = celeb_df_ave['favorite_count_norm'],
        text = celeb_df_ave['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 10
        },
        name = 'celebrity'
)

trace5 = dict(
        type = 'scatterternary',
        a = athlete_df_ave['retweet_count_norm'],
        b = athlete_df_ave['rfr_norm'],
        c = athlete_df_ave['favorite_count_norm'],
        text = athlete_df_ave['screen_name'],
        mode ='markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 10
        },
        name = 'athlete'
)

trace6 = dict(
        type = 'scatterternary',
        a = musician_df_ave['retweet_count_norm'],
        b = musician_df_ave['rfr_norm'],
        c = musician_df_ave['favorite_count_norm'],
        text = musician_df_ave['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 10
        },
        name = 'musician'
)

app.layout = html.Div(children=[

    html.Div(children=[
        html.H1(children='Twitter Persona Likability'),
        html.P(children='Judge Individuals\' Likability Based on Tweeting Habits', style={'font-style': 'italic'}),
        ]
    ),

    html.H2('TwitTernary Plots'),

    dcc.Graph(
        id = 'example-graph',
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'Followers', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
                'annotations': [{
                    'showarrow': False,
                    'text': 'Individual Tweets',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    ),

    dcc.Graph(
        id = 'example-graph-2',
        figure = {
            'data': [trace4, trace5, trace6],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'Followers', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
                'annotations': [{
                    'showarrow': False,
                    'text': 'Average Tweets',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    ),

])

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
