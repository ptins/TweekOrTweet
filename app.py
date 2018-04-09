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

people = pd.read_csv('people_list.csv') # for later
df = pd.read_csv('user_tweets_from.csv', header=None)
df.columns = ['tweet_id','created_at','text','favorite_count','retweet_count','followers_count','screen_name','industry']
df.set_index('tweet_id', inplace=True)

# feature processing
df['rfr'] = (df['favorite_count']+df['retweet_count'])/df['followers_count']

# normalization
tmp = df.drop(['created_at','text','screen_name','industry'],axis=1)
normalized = (tmp-tmp.min())/(tmp.max()-tmp.min())
normalized['text'] = df['text']
normalized['created_at']= df['created_at']
normalized['screen_name']= df['screen_name']
normalized['industry']= df['industry']
df = normalized

## split data into industry for traces
celeb_df = df[df['industry']=='celebrity']
athlete_df = df[df['industry']=='athlete']
musician_df = df[df['industry']=='musician']

# take care of averages
df_ave = df.groupby('screen_name').mean()
df_ave = pd.merge(df_ave, people, left_index=True, right_on='screen_name')

celeb_df_ave = df_ave[df_ave['industry']=='celebrity']
athlete_df_ave = df_ave[df_ave['industry']=='athlete']
musician_df_ave = df_ave[df_ave['industry']=='musician']

trace1 = dict(
        type='scatterternary',
        a = celeb_df['retweet_count'],
        b = celeb_df['rfr'],
        c = celeb_df['favorite_count'],
        text = celeb_df['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 14
        },
        name = 'Celebrities'
)

trace2 = dict(
        type = 'scatterternary',
        a = athlete_df['retweet_count'],
        b = athlete_df['rfr'],
        c = athlete_df['favorite_count'],
        text = athlete_df['screen_name'],
        mode ='markers',
        opacity = .5,
        marker = {
            'symbol': athlete_df['screen_name'],
            'color': 'red',
            'size': 14
        },
        name = 'Athletes'
)

trace3 = dict(
        type = 'scatterternary',
        a = musician_df['retweet_count'],
        b = musician_df['rfr'],
        c = musician_df['favorite_count'],
        text = musician_df['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': musician_df['screen_name'],
            'color': 'blue',
            'size': 14
        },
        name = 'Musicians'
)

trace4 = dict(
        type = 'scatterternary',
        a = celeb_df_ave['retweet_count'],
        b = celeb_df_ave['rfr'],
        c = celeb_df_ave['favorite_count'],
        text = celeb_df_ave['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 14
        },
        name = 'Celebrities'
)

trace5 = dict(
        type = 'scatterternary',
        a = athlete_df_ave['retweet_count'],
        b = athlete_df_ave['rfr'],
        c = athlete_df_ave['favorite_count'],
        text = athlete_df_ave['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 14
        },
        name = 'Athletes'
)

trace6 = dict(
        type = 'scatterternary',
        a = musician_df_ave['retweet_count'],
        b = musician_df_ave['rfr'],
        c = musician_df_ave['favorite_count'],
        text = musician_df_ave['screen_name'],
        mode ='markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 14
        },
        name = 'Musicians'
)

app.layout = html.Div(children=[

    html.Div(children=[

        html.H1(children='Twitter Persona Likability'),
        html.P(children='Judge Individuals\' Likability Based on Tweeting Habits', style={'font-style': 'italic'}),

        ],
        style = {
            'margin':'auto',
            'textAlign': 'center',
            }
    ),

    ## industry selection
    html.Div(children=[

        html.H2('Select Metric:'),
        dcc.Dropdown(
            id='metric',
            options=[
                {'label': 'Reactions/Followers', 'value': 'rfr'},
                {'label': 'User Tweet Polarity', 'value': 'sentiment'}
            ],
            value='rfr'
            ),
        ],
        style = {
                'width':'50%',
                'margin':'auto',
                'textAlign': 'center',
                'marginBottom': 20,
        }
    ),

    html.H2('TwitTernary Plots', style={'textAlign': 'center'}),

    dcc.Graph(
        id = 'example-graph',
        style = {
            'width': '50%',
            'display': 'inline-block'
        },
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'RFR', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
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
        style = {
            'width': '50%',
            'display': 'inline-block'
        },
        figure = {
            'data': [trace4, trace5, trace6],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'RFR', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
                'annotations': [{
                    'showarrow': False,
                    'text': 'Average Across Tweets',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    )



])

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
