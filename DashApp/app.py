import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

df = pd.read_csv('user_tweets_FROM.csv')
df.columns = ['tweet_id','created_at','favorite_count','retweet_count','followers_count','screen_name','industry']
celeb_df = df[df['industry']=='celebrity']
athlete_df = df[df['industry']=='athlete']
musician_df = df[df['industry']=='musician']

trace1 = dict(
        type='scatterternary',
        a= celeb_df['retweet_count'],
        b= celeb_df['retweet_count'],
        c= celeb_df['favorite_count'],
        text= celeb_df['screen_name'],
        mode='markers',
        marker={
            'symbol': 100,
            'color': 'green',
            'size': 10
        }
)

trace2 = dict(
        type='scatterternary',
        a=athlete_df['retweet_count'],
        b=athlete_df['retweet_count'],
        c=athlete_df['favorite_count'],
        text= athlete_df['screen_name'],
        mode='markers',
        marker={
            'symbol': 100,
            'color': 'red',
            'size': 10
        }
)

trace3 = dict(
        type='scatterternary',
        a= musician_df['retweet_count'],
        b= musician_df['retweet_count'],
        c= musician_df['favorite_count'],
        text= musician_df['screen_name'],
        mode='markers',
        marker={
            'symbol': 100,
            'color': 'blue',
            'size': 10
        }
)

app.layout = html.Div(children=[

    html.Div(children=[

        html.H1(children='Twitter Persona Likability'),
        html.P(children='Judge Individuals\' Likability Based on Tweeting Habits'),

    ]),

    html.Div(children=[

        html.H3('Select Industry'),
        dcc.Dropdown(
            options=[
                {'label': 'Celebrities', 'value': 'celebrity'},
                {'label': 'Athletes', 'value': 'athlete'},
                {'label': 'Musicians', 'value': 'musician'}
            ],
            value=['celebrity', 'athlete', 'musician'],
            multi=True
            )
        ]
    ),


    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1],
            # 'data': [trace1, trace2, trace3],
            'layout': {
                'title': 'Ternary Scatter Plot',
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'X', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'W', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'S', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
