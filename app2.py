import numpy as np
import pandas as pd
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

## start app

app = dash.Dash(__name__)
server = app.server

df_people = pd.read_csv('people_list.csv')

### FROM DF ###

df_from = pd.read_csv('user_tweets_from.csv')
df_about = pd.read_csv('user_tweets_about.csv')

df_from['daysSince'] = (datetime.utcnow() - pd.to_datetime(df_from['created_at'])).dt.days
df_about['daysSince'] = (datetime.utcnow() - pd.to_datetime(df_about['created_at'])).dt.days

app.layout = html.Div(children=[

    html.Div(id='some-text'),

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
])

@app.callback(
    Output(component_id='some-text', component_property='children'),
    [Input(component_id='daysSince-slider', component_property='value')]
)
def update_output_div(daysSince):
    return 'You want to get tweets from {} days ago.'.format(daysSince)



if __name__ == '__main__':
    app.run_server(debug=False)
