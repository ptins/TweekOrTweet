import pandas as pd

from sklearn.metrics import confusion_matrix, accuracy_score

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server

df_people = pd.read_csv('people_list.csv')

# get all search choices for individual search box
labels = df_people['industry'].unique()
options = []
for label in labels:
    options.append(dict({'label':label.capitalize(), 
                         'value':label}))
    
first = df_people['industry'][0]    

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

df_from = df_from.groupby('screen_name').mean()
df_from = pd.merge(df_from, df_people, left_index=True, right_on='screen_name')

df_from_first = df_from[df_from['industry']==first]

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
            'color': df_from_first['controversial'],
            'size': 10
        },
        name = first
)

### END FROM SECTION ###

### START ABOUT SECTION ###

# read in data
df_about = pd.read_csv('user_tweets_about.csv', index_col='tweet_id')

## normalization
# split into numeric and non-numeric
numeric = df_about.drop(['created_at','text','screen_name'],axis=1)
non_numeric = df_about[['created_at','text','screen_name']]
# normalize numeric
numeric_norm = numeric.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)
# merge back together
df_about = pd.merge(numeric_norm, non_numeric, left_index=True, right_index=True)

df_about = df_about.groupby('screen_name').mean()
df_about = pd.merge(df_about, df_people, left_index=True, right_on='screen_name')

# compute controversiality
df_about['controversiality'] = 19.864-35.465*df_about['polarity']+620.196*df_about['favorite_count']

# set initial conditions
df_about_first = df_about[df_about['industry']==first]

trace_about = go.Scatter(
    x = df_about_first['screen_name'],
    y = df_about_first['controversiality'],
    mode = 'markers',
    name = first
)

### END ABOUT SECTION ###

### CLASSIFICATION RESULTS ###

df_from['rfr_pred'] = df_from['rfr']<df_from['rfr'].mean()

print('\n### RFR ###\n')

print('ConfMat (Total):\n{}'.format(
    confusion_matrix(
        df_from['controversial'], 
        df_from['rfr_pred'])))
print('Accuracy: {}'.format(accuracy_score(
        df_from['controversial'], 
        df_from['rfr_pred'])))

print('ConfMat (Celebrity):\n{}'.format(
    confusion_matrix(
        df_from[df_from['industry']=='celebrity']['controversial'], 
        df_from[df_from['industry']=='celebrity']['rfr_pred'])))
      
print('Accuracy: {}'.format(
    accuracy_score(
        df_from[df_from['industry']=='celebrity']['controversial'], 
        df_from[df_from['industry']=='celebrity']['rfr_pred'])))      

print('ConfMat (Athlete):\n{}'.format(
    confusion_matrix(
        df_from[df_from['industry']=='athlete']['controversial'], 
        df_from[df_from['industry']=='athlete']['rfr_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_from[df_from['industry']=='athlete']['controversial'], 
        df_from[df_from['industry']=='athlete']['rfr_pred'])))      
      
print('ConfMat (Musician):\n{}'.format(
    confusion_matrix(
        df_from[df_from['industry']=='musician']['controversial'], 
        df_from[df_from['industry']=='musician']['rfr_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_from[df_from['industry']=='musician']['controversial'], 
        df_from[df_from['industry']=='musician']['rfr_pred'])))      
      
df_about['controversial_pred'] = df_about['controversiality']>df_about['controversiality'].mean()
print('\n### Controversiality Metric ###\n')
print('ConfMat (Total):\n{}'.format(
    confusion_matrix(
        df_about['controversial'], 
        df_about['controversial_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_about['controversial'], 
        df_about['controversial_pred'])))

print('ConfMat (Celebrity):\n{}'.format(
    confusion_matrix(
        df_about[df_about['industry']=='celebrity']['controversial'], 
        df_about[df_about['industry']=='celebrity']['controversial_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_about[df_about['industry']=='celebrity']['controversial'], 
        df_about[df_about['industry']=='celebrity']['controversial_pred'])))

print('ConfMat (Athlete):\n{}'.format(
    confusion_matrix(
        df_about[df_about['industry']=='athlete']['controversial'], 
        df_about[df_about['industry']=='athlete']['controversial_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_about[df_about['industry']=='athlete']['controversial'], 
        df_about[df_about['industry']=='athlete']['controversial_pred'])))

print('ConfMat (Musician):\n{}'.format(
    confusion_matrix(
        df_about[df_about['industry']=='musician']['controversial'], 
        df_about[df_about['industry']=='musician']['controversial_pred'])))
print('Accuracy: {}'.format(
    accuracy_score(
        df_about[df_about['industry']=='musician']['controversial'], 
        df_about[df_about['industry']=='musician']['controversial_pred'])))


### END CLASSIFICATION RESULTS ###

app.layout = html.Div(children=[

    # header
    html.Div(children=[
        
        html.H1('Twitter Persona Likability'),
        html.H3('By Industry'),
        html.H5('Version 1.0'),
    
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
def update_figure(industry):
        
    # filter df_from
    df_from_filtered = df_from[df_from['industry'] == industry]
    
    trace_from = dict(
        type='scatterternary',
        a = df_from_filtered['retweet_count'],
        b = df_from_filtered['rfr'],
        c = df_from_filtered['favorite_count'],
        text = df_from_filtered['screen_name'],
        mode = 'markers',
        marker = {
            'symbol': 'o',
            'size': 10,
            'color': df_from_filtered['controversial'],
            'colorscale':'Jet',
        },
        name = industry
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
                    'text': industry.capitalize(),
                    'x': 0.5,
                    'y': 1.3,
                    'font': { 'size': 25 }
                }]
            }
        }


@app.callback(
    dash.dependencies.Output('controversiality-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(industry):
        
    # filter df_about
    df_about_filtered = df_about[df_about['industry'] == industry]
                
    trace_about = go.Scatter(
        x = df_about_filtered['screen_name'],
        y = df_about_filtered['controversiality'],
        mode = 'markers',
        name = industry,
        marker = dict(
            size=14,
            cmin=0,
            cmax=1,
            color = df_about_filtered['controversial'],
            colorscale='Jet',
        )
    )

    return {
            'data': [trace_about],
            'layout': {'title': industry.capitalize()}
        }

if __name__ == '__main__':
    app.run_server(debug=False)
