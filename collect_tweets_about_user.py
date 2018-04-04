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

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def collect_tweets_about_user(screen_name, industry):

    print('collecting tweets about '+screen_name)

    # fetch tweets
    tweets = api.search(screen_name, lang='en', count=200)

    try:

        # open file
        with open('user_tweets_about.csv', 'a') as myfile:

            # loop through tweets
            for tweet in tweets:

                clean_text = clean_tweet(tweet.text)
                analysis = TextBlob(clean_text)
                polarity = analysis.sentiment.polarity

                # make sure tweet not already in file
                if str(tweet.id) not in open('user_tweets_about.csv').read():

                    s = '{},{},{},{},{},{},{},{}\n'.format(tweet.id,
                                                        tweet.created_at,
                                                        tweet.favorite_count,
                                                        tweet.retweet_count,
                                                        clean_text,
                                                        polarity,
                                                        screen_name,
                                                        industry)
                    # write to file
                    myfile.write(s)

    except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


people = pd.read_csv('people_list.csv')

### ONLY LINE NEED TO CHANGE -- 'celebrity' to 'athlete/musician'
industry = 'celebrity'
###

screen_names = list(people[people['industry']==industry]['screen_name'])
[collect_tweets_about_user(screen_name, industry) for screen_name in screen_names]
