def write_from_user_tweets_to_file(screen_name):

    # fetch tweets
    # tweets = api.user_timeline(screen_name, count=200)
    tweets = api.user_timeline(screen_name, count=50)
    
    try:
        
        # open file
        with open('from_user_tweets.csv', 'a') as myfile:
            
            clean_text = tweet.text.translate(None, string.punctuation)
            
            # loop through tweets
            for tweet in tweets:
                s = '{}~{}~{}~{}~{}~{}~{}\n'.format(tweet.id, tweet.created_at, clean_text,
                                                tweet.favorite_count, tweet.retweet_count, 
                                                tweet.user.screen_name, tweet.user.followers_count)        
                # write to file
                myfile.write(s)
                
    except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
    
class StreamListener(tweepy.StreamListener):
    
    def __init__(self):
        self.num_tweets = 0
        super(StreamListener, self).__init__()        
    
    def on_status(self, tweet): 
        
        if self.num_tweets < 50:

            with open('about_user_tweets.csv', 'a') as tf:
                    
                s = '{},{},{},{},{},{},{}\n'.format(tweet.id, tweet.created_at, tweet.text,
                                                    tweet.favorite_count, tweet.retweet_count, 
                                                    tweet.user.screen_name, tweet.user.followers_count)
                tf.write(s)
                self.num_tweets += 1
                print(self.num_tweets)
                
            return True
        else:
            return False
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        
def write_about_user_tweets_to_file(screen_name):

    # set up streaming
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    # stream and collect about username
    stream.filter(track=[screen_name], async=True)
    
def ternary_plot(df):

    data = [{ 
        'type': 'scatterternary',
        'mode': 'markers',
        'a': df['retweet_count'],
        'b': df['rfr'],
        'c': df['favorite_count'],
        'text': df['text'],
        'marker': {
            'symbol': 'x',
            'color': df['screen_name_ind'],
            'autocolorscale': True,
            'size': 12
        }
    }]

    layout = {
        'ternary': {
            'sum': 1,
            'aaxis': makeAxis('Retweets'),
            'baxis': makeAxis('<br>RFR'),
            'caxis': makeAxis('<br>Favorites')
        },
        'annotations': [{
            'showarrow': False,
            'text': 'Test',
            'x': 0.5,
            'y': 1.3,
            'font': { 'size': 35 }
        }]
    }

    fig = {'data': data, 'layout': layout}
    offline.iplot(fig, validate=False)
    
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