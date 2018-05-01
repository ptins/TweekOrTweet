import pandas as pd
from scipy import signal

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

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

    
first = df_people['screen_name'][0]

### START FROM SECTION ###   

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

df_from_first = df_from[df_from['screen_name']==first]

trace_from = dict(
        type='scatterternary',
        a = df_from_first['retweet_count'],
        b = df_from_first['rfr'],
        c = df_from_first['favorite_count'],
        text = df_from_first['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 10
        },
        name = first
)

### END FROM SECTION ###



### START ABOUT SECTION ###

# read in data
df_about = pd.read_csv('user_tweets_about.csv', index_col='tweet_id')


# compute controversiality
df_about['controversiality'] = 5.220e-02-6.307e-01*df_about['polarity']-1.664e-06*df_about['retweet_count']


## normalization
# split into numeric and non-numeric
numeric = df_about.drop(['created_at','text','screen_name'],axis=1)
non_numeric = df_about[['created_at','text','screen_name']]
# normalize numeric
numeric_norm = numeric.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)
# merge back together
df_about = pd.merge(numeric_norm, non_numeric, left_index=True, right_index=True)

# set initial conditions
df_about_first = df_about[df_about['screen_name']==first]

trace_about = go.Scatter(
    x = df_about_first['created_at'],
    y = df_about_first['controversiality'],
    mode = 'markers+lines',
    name = first
)


### END ABOUT SECTION ###
    
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
            value=first,
        ),
        
    ]),
    
    # ternary plot
    dcc.Graph(
        id = 'ternary-plot',
        figure = {
            'data': [trace_from],
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
    
    # controversiality plot
    dcc.Graph(
        id = 'controversiality-plot',
        figure = {
            'data': [trace_about],
            'layout': {'title': '<Individual>'}

        }
    ),
    
    
])

@app.callback(
    dash.dependencies.Output('ternary-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(screen_name):
        
    # filter df_from
    df_from_filtered = df_from[df_from['screen_name'] == screen_name]
    
    trace_from = dict(
        type='scatterternary',
        a = df_from_filtered['retweet_count'],
        b = df_from_filtered['rfr'],
        c = df_from_filtered['favorite_count'],
        text = df_from_filtered['screen_name'],
        mode = 'markers',
        opacity = .5,
        marker = {
            'symbol': 'o',
            'color': 'blue',
            'size': 10
        },
        name = screen_name
    )

    return {
            'data': [trace_from],
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


@app.callback(
    dash.dependencies.Output('controversiality-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(screen_name):
        
    # filter df_about
    df_about_filtered = df_about[df_about['screen_name'] == screen_name]
    
    trace_about = go.Scatter(
        x = df_about_filtered['created_at'],
        y = df_about_filtered['controversiality'],
        mode = 'markers+lines',
        name = screen_name
    )

    return {
            'data': [trace_about],
            'layout': {'title': screen_name}
        }

if __name__ == '__main__':
    app.run_server(debug=False)
