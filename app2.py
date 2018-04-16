import numpy as np
import pandas as pd
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

## functions

def split_df_by_industry(df):
    df1 = df.loc[df['industry'] == 'athlete']
    df2 = df.loc[df['industry'] == 'celebrity']
    df3 = df.loc[df['industry'] == 'musician']
    return df1, df2, df3

def split_df_by_controversy(df):
    df1 = df.loc[df['controversial'] == 0]
    df2 = df.loc[df['controversial'] == 1]
    return df1, df2

## start app

app = dash.Dash(__name__)
server = app.server

df_people = pd.read_csv('people_list.csv')

### FROM DF ###

df_from = pd.read_csv('user_tweets_from.csv')
df_about = pd.read_csv('user_tweets_about.csv')

df_from['rfr'] = (df_from['favorite_count']+df_from['retweet_count'])/df_from['followers_count']

df_from['favorite_count_norm'] = df_from['favorite_count'] / df_from['favorite_count'].max()
df_from['retweet_count_norm']  = df_from['retweet_count'] / df_from['retweet_count'].max()
df_from['followers_count_norm'] = df_from['followers_count'] / df_from['followers_count'].max()
df_from['rfr_norm'] = df_from['rfr'] / df_from['rfr'].max()

df_from = pd.merge(left=df_from, right=df_people)
# df_about = pd.merge(left=df_about, right=df_people)

df_from_individual = pd.merge(left=df_from.groupby('screen_name').mean(),
                            right=df_people.drop('controversial',axis=1),
                            left_index=True, right_on='screen_name')
# df_about_individual = df_about.groupby('screen_name').mean()
print(df_from_individual.head())
# exit()

df_from_athlete, df_from_celebrity, df_from_musician = split_df_by_industry(df_from)
# df_about_athlete, df_about_celebrity, df_about_musician = split_df_by_industry(df_about)

df_from_athlete_individual, df_from_celebrity_individual, df_from_musician_individual = split_df_by_industry(df_from_individual)
# df_about_athlete_individual, df_about_celebrity_individual, df_about_musician_individual = split_df_by_industry(df_about_individual)

trace1 = dict(
        type='scatterternary',
        a = df_from_athlete['retweet_count_norm'],
        b = df_from_athlete['rfr_norm'],
        c = df_from_athlete['favorite_count_norm'],
        text = df_from_athlete['text'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 10
        },
        name = 'Athlete'
)

trace2 = dict(
        type='scatterternary',
        a = df_from_celebrity['retweet_count_norm'],
        b = df_from_celebrity['rfr_norm'],
        c = df_from_celebrity['favorite_count_norm'],
        text = df_from_celebrity['text'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 10
        },
        name = 'Celebrity'
)

trace3 = dict(
        type='scatterternary',
        a = df_from_musician['retweet_count_norm'],
        b = df_from_musician['rfr_norm'],
        c = df_from_musician['favorite_count_norm'],
        text = df_from_musician['text'],
        mode = 'markers',
        opacity = .75,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 10
        },
        name = 'Musician'
)

trace4 = dict(
        type='scatterternary',
        a = df_from_athlete_individual['retweet_count_norm'],
        b = df_from_athlete_individual['rfr_norm'],
        c = df_from_athlete_individual['favorite_count_norm'],
        text = df_from_athlete_individual['screen_name'],
        mode = 'markers',
        opacity = .75,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 10
        },
        name = 'Athlete'
)

trace5 = dict(
        type='scatterternary',
        a = df_from_celebrity_individual['retweet_count_norm'],
        b = df_from_celebrity_individual['rfr_norm'],
        c = df_from_celebrity_individual['favorite_count_norm'],
        text = df_from_celebrity_individual['screen_name'],
        mode = 'markers',
        opacity = .75,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 10
        },
        name = 'Celebrity'
)

trace6 = dict(
        type='scatterternary',
        a = df_from_musician_individual['retweet_count_norm'],
        b = df_from_musician_individual['rfr_norm'],
        c = df_from_musician_individual['favorite_count_norm'],
        text = df_from_musician_individual['screen_name'],
        mode = 'markers',
        opacity = .75,
        marker = {
            'symbol': 'o',
            'color': 'green',
            'size': 10
        },
        name = 'Musician'
)

app.layout = html.Div(children=[

    html.H3(id='some-text'),

    html.Div([
        dcc.Slider(
            id='daysSince-slider',
            min=0,
            max=30,
            value=10,
            step=None,
            marks={str(i): str(i) for i in np.arange(0,30,1)}
        ),
    ]),

    html.Br(),
    html.Br(),

    dcc.Graph(
        id = 'graph-1',
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
                    'text': 'TwitTernary (All Tweets)',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    ),

    dcc.Graph(
        id = 'graph-2',
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
                    'text': 'TwitTernary (Average Tweets)',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    ),

])

@app.callback(
    Output(component_id='some-text', component_property='children'),
    [Input(component_id='daysSince-slider', component_property='value')]
)
def update_output_div(daysSince):
    return 'You want to get tweets from {} days ago.'.format(daysSince)

if __name__ == '__main__':
    app.run_server(debug=False)
