import pandas as pd

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

### START FROM SECTION ###
    
# read in data
df_about = pd.read_csv('user_tweets_about.csv', index_col='tweet_id')

# compute likability
df_about['likability'] = 1-(5.220e-02-6.307e-01*df_about['polarity']-1.664e-06*df_about['retweet_count'])

## normalization
# split into numeric and non-numeric
numeric = df_about.drop(['created_at','text','screen_name'],axis=1)
non_numeric = df_about[['created_at','text','screen_name']]
# normalize numeric
numeric_norm = numeric.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)
# merge back together
df_about = pd.merge(numeric_norm, non_numeric, left_index=True, right_index=True)

# set initial conditions
first = df_people['screen_name'][0]
df_about_first = df_about[df_about['screen_name']==first]

trace = go.Scatter(
    x = df_about_first['created_at'],
    y = df_about_first['likability'],
    mode = 'markers+lines',
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
            value=first,
        ),
        
    ]),
    
    # likability plot
    dcc.Graph(
        id = 'likability-plot',
        figure = {
            'data': [trace],
            'layout': {'title': '<Individual>'}

        }
    ),
    
    
])

@app.callback(
    dash.dependencies.Output('likability-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(screen_name):
        
    # filter df_about
    df_about_filtered = df_about[df_about['screen_name'] == screen_name]
    
    trace = go.Scatter(
        x = df_about_filtered['created_at'],
        y = df_about_filtered['likability'],
        mode = 'markers+lines',
        name = screen_name
    )

    return {
            'data': [trace],
            'layout': {'title': screen_name}
        }

if __name__ == '__main__':
    app.run_server(debug=False)
