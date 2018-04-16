import re
import tweepy
import pandas as pd
from textblob import TextBlob
from sklearn import preprocessing

import preprocessor as p
p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY)

import string

consumer_key = 'n9LMcL7CRMtaTY5TXMp1VfIKo'
consumer_secret = 'G0ghn8E8TJPCKl29AfmA4019U1hq6NhGQFoMsJ05CARnmkeE7U'
access_token = '1959972582-gfpDYaAbKj7c412HOalcL0jQv0QdhJtgwZguXjl'
access_token_secret = 'nZJVEdDSHsCZvV8dvRtXBjOoDIzeKOSKyvtaavjeV5ARK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)

people = pd.read_csv('people_list.csv')

def clean_tweet(tweet):
    t = p.clean(tweet)
    table = t.maketrans({key: None for key in string.punctuation})
    return t.translate(table)

def collect_tweets_from_user(screen_name):

    print('collecting tweets from '+screen_name)

    industry = people[people['screen_name']==screen_name]['industry'].values[0]

    # fetch tweets
    tweets = api.user_timeline(screen_name, count=200)

    try:

        # open file
        with open('user_tweets_from.csv', 'a') as myfile:

            # loop through tweets
            for tweet in tweets:

                # check if tweet in file
                if str(tweet.id) not in open('user_tweets_from.csv').read():

                    clean_text = clean_tweet(tweet.text)

                    s = '{},{},{},{},{},{},{}\n'.format(tweet.id,
                                                     tweet.created_at,
                                                     clean_text,
                                                     tweet.favorite_count,
                                                     tweet.retweet_count,
                                                     tweet.user.followers_count,
                                                     tweet.user.screen_name)
                    # write to file
                    myfile.write(s)

    except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

screen_names = list(people['screen_name'])
[collect_tweets_from_user(screen_name) for screen_name in screen_names]
