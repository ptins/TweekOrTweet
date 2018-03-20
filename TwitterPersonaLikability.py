
import pandas as pd
from pprint import pprint

import os, json, tweepy

consumer_key        = 'n9LMcL7CRMtaTY5TXMp1VfIKo'
consumer_secret     = 'G0ghn8E8TJPCKl29AfmA4019U1hq6NhGQFoMsJ05CARnmkeE7U'
access_token        = '1959972582-gfpDYaAbKj7c412HOalcL0jQv0QdhJtgwZguXjl'
access_token_secret = 'nZJVEdDSHsCZvV8dvRtXBjOoDIzeKOSKyvtaavjeV5ARK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)

# pprint(api.get_status(972194214841864194)._json)

def get_replies(tweet_id):

    # store replies in replies.jsonl
    code = 'twarc replies '+str(tweet_id)+' > replies.jsonl'
    os.system(code)

    # get number of replies
    with open('replies.jsonl') as f:
        content = f.readlines()

    # only get text
    tweets = [json.loads(line)['full_text'] for line in content]
    return(tweets)

def like_rt_replies(tweet_id):

    # get Status object
    status = api.get_status(tweet_id)._json

    # get easy statistics
    user = status['user']['screen_name']
    text = status['text']
    num_likes = status['favorite_count']
    num_rt = status['retweet_count']

    # get replies
    rep = get_replies(tweet_id)

    '''
    Ultimately, this is where we'll do some sentiment analysis-type stuff.
    '''

    num_rep = len(rep)+1

    # compute 'The Ratio'
    ratio = (num_likes+num_rt) / num_rep

    # return list of statistics
    return([user, text, num_likes, num_rt, num_rep, ratio])



def makeAxis(title):
    return {
      'title': title,
      'titlefont': { 'size': 20 },
      'tickfont': { 'size': 15 },
      'tickcolor': 'rgba(0,0,0,0)',
      'ticklen': 5,
      'showline': True,
      'showgrid': True
    }

def ternary_plot(df, name):

    data = [{
        'type': 'scatterternary',
        'mode': 'markers',
        'a': df['rt'],
        'b': df['rep'],
        'c': df['fav'],
        'text': df['text'],
        'marker': {
            'symbol': 'circle',
            'size': 15,
            'line': { 'width': 2 }
        }
    }]

    layout = {
        'ternary': {
            'sum': 1,
            'aaxis': makeAxis('Retweets'),
            'baxis': makeAxis('<br>Replies'),
            'caxis': makeAxis('<br>Likes')
        },
        'annotations': [{
          'showarrow': False,
          'text': name,
            'x': 0.5,
            'y': 1.3,
            'font': { 'size': 35 }
        }]
    }

    fig = {'data': data, 'layout': layout}
    offline.iplot(fig, validate=False)

def gather_data_and_plot(username):

    print('Starting with '+username+'...')
    tmpdf = pd.DataFrame(columns=['user','text','fav','rt','rep','ratio'])

    for status in api.user_timeline(username):
        print(status.id)
        # append to end of dataframe
        tmpdf.loc[-1] = like_rt_replies(status.id)
        tmpdf.index = tmpdf.index + 1  # shifting index
        tmpdf = tmpdf.sort_index()

    # print(tmpdf)
    ternary_plot(tmpdf, username)

    return(tmpdf)

gather_data_and_plot('tomhanks')
