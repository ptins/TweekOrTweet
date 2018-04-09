import re
import tweepy
import pandas as pd
from textblob import TextBlob
from sklearn import preprocessing

consumer_key = 'n9LMcL7CRMtaTY5TXMp1VfIKo'
consumer_secret = 'G0ghn8E8TJPCKl29AfmA4019U1hq6NhGQFoMsJ05CARnmkeE7U'
access_token = '1959972582-gfpDYaAbKj7c412HOalcL0jQv0QdhJtgwZguXjl'
access_token_secret = 'nZJVEdDSHsCZvV8dvRtXBjOoDIzeKOSKyvtaavjeV5ARK'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api  = tweepy.API(auth)

import preprocessor as p
def clean_tweet(tweet):
    return p.clean(tweet).replace(',',' ')

def collect_tweets_from_user(screen_name, industry):

    print('collecting tweets from '+screen_name)

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

                    s = '{},{},{},{},{},{},{},{}\n'.format(tweet.id,
                                                     tweet.created_at,
                                                     clean_text,
                                                     tweet.favorite_count,
                                                     tweet.retweet_count,
                                                     tweet.user.followers_count,
                                                     tweet.user.screen_name,
                                                     industry)
                    # write to file
                    myfile.write(s)

    except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


people = pd.read_csv('people_list.csv')

def collect_for_industry(industry):
    screen_names = list(people[people['industry']==industry]['screen_name'])
    # print(screen_names)
    [collect_tweets_from_user(screen_name, industry) for screen_name in screen_names]

[collect_for_industry(industry) for industry in ['celebrity','athlete','musician']]
