import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

df = pd.read_csv('user_tweets_FROM.csv')
df.columns = ['tweet_id','created_at','favorite_count','retweet_count','followers_count','screen_name','industry']

trace1 = dict(
        type='scatterternary',
        a= df['retweet_count'],
        b= df['retweet_count'],
        c= df['favorite_count'],
        text= df['screen_name'],
        mode='markers',
        marker={
            'symbol': 100,
            'color': 'green',
            'size': 10
        }
)

# trace2 = dict(
#         type='scatterternary',
#         a=[4, 5, 6],
#         b=[5, 6, 7],
#         c=[6, 7, 8],
#         mode='markers',
#         marker={
#             'symbol': 100,
#             'color': 'red',
#             'size': 10
#         }
# )
#
# trace3 = dict(
#         type='scatterternary',
#         a=[7, 8, 9],
#         b=[8, 9, 10],
#         c=[9, 10, 11],
#         mode='markers',
#         marker={
#             'symbol': 100,
#             'color': 'blue',
#             'size': 10
#         }
# )

app.layout = html.Div(children=[

    html.Div(children=[

        html.H1(children='Twitter Persona Likability'),
        html.P(children='Judge Individuals\' Likability Based on Tweeting Habits'),

    ]),

    html.Div(children=[

        html.H3('Select Industry'),
        dcc.Dropdown(
            options=[
                {'label': 'Celebrities', 'value': 'CEL'},
                {'label': 'Athletes', 'value': 'ATH'},
                {'label': 'Musicians', 'value': 'MUS'}
            ],
            value=['CEL', 'ATH'],
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
