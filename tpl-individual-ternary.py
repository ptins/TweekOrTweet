import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
server = app.server

df_people = pd.read_csv('people_list.csv')

# get all search choices for individual search box
labels = df_people['name']
values = df_people['screen_name']
values2 = df_people['industry']
options = []
for label, value, value2 in zip(labels, values, values2):
    options.append(dict({'label':label+' - '+(value2.capitalize()), 
                         'value':value}))

# read in data
df_from = pd.read_csv('user_tweets_from.csv', index_col='tweet_id')

# compute rfr
df_from['rfr'] = (df_from['favorite_count']+df_from['retweet_count'])/df_from['followers_count']

## normalization
# split into numeric and non-numeric
numeric = df_from.drop(['created_at','text','screen_name','followers_count'],axis=1)
non_numeric = df_from[['created_at','text','screen_name']]
# normalize numeric
numeric_norm = numeric.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)
# merge back together
df_from = pd.merge(numeric_norm, non_numeric, left_index=True, right_index=True)

# set initial conditions
first = df_people['screen_name'][0]
df_from_first = df_from[df_from['screen_name']==first]

trace = dict(
        type='scatterternary',
        a = df_from_first['retweet_count'],
        b = df_from_first['rfr'],
        c = df_from_first['favorite_count'],
        text = df_from_first['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 10
        },
        name = first
)
    
app.layout = html.Div(children=[

    # header
    html.Div(children=[
        
        html.H1('Twitter Persona Likability'),
        html.H3('Individual Version 1.0'),
    
    ]),
    
    # search box
    html.Div(children=[
                
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value=first
        ),
        
    ]),
    
    # ternary plot
    dcc.Graph(
        id = 'ternary-plot',
        figure = {
            'data': [trace],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'RFR', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
                'annotations': [{
                    'showarrow': False,
                    'text': '<Individual>',
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }
    ),
    
])

@app.callback(
    dash.dependencies.Output('ternary-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(screen_name):
        
    # filter df_from
    df_from_filtered = df_from[df_from['screen_name'] == screen_name]
    
    trace = dict(
        type='scatterternary',
        a = df_from_filtered['retweet_count'],
        b = df_from_filtered['rfr'],
        c = df_from_filtered['favorite_count'],
        text = df_from_filtered['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'red',
            'size': 10
        },
        name = screen_name
    )

    return {
            'data': [trace],
            'layout': {
                'ternary': {
                    'sum': 1,
                    'aaxis': {'title': 'Retweet Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'baxis': {'title': 'RFR', 'min': 0.01, 'linewidth':2, 'ticks':'outside' },
                    'caxis': {'title': 'Favorite Count', 'min': 0.01, 'linewidth':2, 'ticks':'outside' }
                },
                'annotations': [{
                    'showarrow': False,
                    'text': screen_name,
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }


if __name__ == '__main__':
    app.run_server(debug=False)
