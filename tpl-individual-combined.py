import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from sklearn.metrics import confusion_matrix, accuracy_score

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



# read in data
df_about = pd.read_csv('user_tweets_about.csv', index_col='tweet_id')

# compute controversiality
df_about['controversiality'] = 5.220e-02-6.307e-01*df_about['polarity']-1.664e-06*df_about['retweet_count']

# merge with people to get controversial information
df_about = pd.merge(df_about, df_people)

## normalization
# split into numeric and non-numeric
numeric = df_about.drop(['created_at','text','screen_name','name','industry'],axis=1)
non_numeric = df_about[['created_at','text','screen_name','name','industry']]
# normalize numeric
numeric_norm = numeric.apply(lambda x: (x-x.min())/(x.max()-x.min()), axis=0)
# merge back together
df_about = pd.merge(numeric_norm, non_numeric, left_index=True, right_index=True)

# get initial
first = df_people['screen_name'][0] 
df_about_first = df_about[df_about['screen_name']==first]

# resampling technique
df_about_first['created_at'] = pd.to_datetime(df_about_first['created_at'])
df_about_first = df_about_first.set_index('created_at').resample('D').mean()
df_about_first.fillna(df_about_first['controversiality'].mean(), inplace=True)
# print(df_about_first)
# exit()

trace_about = go.Scatter(
    x = df_about_first.index,
    y = df_about_first['controversiality'],
    mode = 'markers+lines',
    name = first
)

app.layout = html.Div(children=[

    # header
    html.Div(children=[
        
        html.H1('Twitter Persona Likability'),
        html.H3('By Individual'),
        html.H5('Version 1.0'),
    
    ]),
    
    # search box
    html.Div(children=[
                
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value=first,
            multi=True,
        ),
        
    ]),
    
    # controversiality plot
    dcc.Graph(
        id = 'controversiality-plot',
        figure = {
            'data': [trace_about],
            'layout': {'title': '<Individual>'}

        }
    ),
    
    
])


# @app.callback(
#     dash.dependencies.Output('controversiality-plot', 'figure'),
#     [dash.dependencies.Input('dropdown', 'value')])
# def update_figure(screen_name):
    
#     # filter df_about
#     df_about_filtered = df_about[df_about['screen_name'] == screen_name]
    
#     # resampling technique
#     df_about_filtered['created_at'] = pd.to_datetime(df_about_filtered['created_at'])
#     df_about_filtered = df_about_filtered.set_index('created_at').resample('D').mean()
#     df_about_filtered.fillna(df_about_filtered['controversiality'].mean(), inplace=True)
    
#     trace_about = go.Scatter(
#         x = df_about_filtered.index,
#         y = df_about_filtered['controversiality'],
#         mode = 'markers+lines',
#         name = screen_name
#     )

#     return {
#             'data': [trace_about],
#             'layout': {'title': screen_name}
#         }

@app.callback(
    dash.dependencies.Output('controversiality-plot', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(screen_name_list):
    
    df_about_filtered = pd.DataFrame()
    traces = []
    title = 'hey there'
    
    if isinstance(screen_name_list, str):
        
        df_about_filtered = df_about[df_about['screen_name'] == screen_name_list]
        df_about_filtered['created_at'] = pd.to_datetime(df_about_filtered['created_at'])
        df_about_filtered = df_about_filtered.set_index('created_at').resample('D').mean()
        df_about_filtered.fillna(df_about_filtered['controversiality'].mean(), inplace=True)
        
        trace = go.Scatter(
            x = df_about_filtered.index,
            y = df_about_filtered['controversiality'],
            mode = 'markers+lines',
            name = screen_name_list
        )
        
        traces.append(trace)
        title = screen_name_list
        
    else:

        for screen_name in screen_name_list:

            tmpdf = df_about[df_about['screen_name'] == screen_name]
            tmpdf['created_at'] = pd.to_datetime(tmpdf['created_at'])
            tmpdf = tmpdf.set_index('created_at').resample('D').mean()
            tmpdf.fillna(tmpdf['controversiality'].mean(), inplace=True)
            df_about_filtered = df_about_filtered.append(tmpdf)

            tmpt = go.Scatter(
                x = tmpdf.index,
                y = tmpdf['controversiality'],
                mode = 'markers+lines',
                name = screen_name
            )
            traces.append(tmpt)
            title = ' vs. '.join(screen_name_list)
            
    return {
            'data': traces,
            'layout': {'title': title}
        }

if __name__ == '__main__':
    app.run_server(debug=False)
