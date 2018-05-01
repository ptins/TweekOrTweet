# Twitter Persona Likability

> The goal of this project was to classify whether or not a Twitter persona is controversial or not with Python.

Course: CSE 60437 - Social Sensing and Cyber-Physical Systems @ the University of Notre Dame.

## Timeline

### Pre-Midterm

1. Determined which Twitter personas we would follow, 20 from each category: celebrities, athletes, and musicians. The subjects were chosen with a degree of subjectivity, but were reinforced by classmates and online articles/surveys.

2. Established data collection technique with two different scripts: collect_tweets_from_user.py and collect_tweets_about_user.py. These were run with a degree of regularity, and the results were written to the files: user_tweets_from.csv and user_tweets_about.csv, respectively.

3. Implemented ternary graph (individual tweets and averaged) for the "celebrity" category. The baseline metric for determining if an individual was controversial was what we called RFR (reactions-per-total follower ratio), which is the number of retweets and favorites divided by the sending user's follower count.

Note: At this point in time, the likability/controversiality of an individual has nothing to do with the content of his or her tweets nor the content of the tweets ABOUT him or her, which will be explored in the next part of the project.

### Post-Midterm

1. Implemented ternary graphs (individual tweets and averaged) for the remaining two "industry" categories (athletes & musicians) based on RFR.

2. Evaluated results for assessing persona controversiality on RFR only. Very poor. Accuracy of ~50%. Confusion matrix for individual tweets can be seen below.

3. Devised our first non-trivial 'controversiality' ratio, using our user_tweets_about data in R and RStudio. We quickly discovered that RFR was not the best indicator of controversiality; features extracted from the user_tweets_from.csv. In other words, what an individual tweets his or herself is of little importance. Using the 'leaps' package in R, we conducted a bidirectional feature subset search on the user_tweets_about data. We finalized a formula for "controversiality" that looked like this: 

![alt text](controversiality2.gif)

## Running the Code

### Grouped by Industry

The first Dash app demonstration shows an average of tweets we've collected for categories of individuals. The ternary graph uses RFR while the second graph shows our 'controversiality' metric; the results be seen by running the following code. Use the dropdown menu and search functionality to select the category of Twitter personas you are most interested in.

```
python tpl-industry-combined.py
```

#### Results (RFR)

Total - Accuracy: ~.5

Celebrity - Accuracy: .65

Athlete - Accuracy: ~.47

Musician - Accuracy: .4

#### Results (Controversiality Metric)

Total - Accuracy: ~0.69

Celebrity - Accuracy: .65

Athlete - Accuracy: ~.76

Musician - Accuracy: .65

### Grouped by Individual

The first graph demonstration encompasses every tweet we've collected in our assessment of whether or not an individual is controversial or not. To see the graphs produced using RFR and this aforementioned 'controversiality' ratio, run the following code to generate an app hosted on localhost:8050. Use the dropdown menu and search functionality to select the person(s) you are most interested in. The second of the two graphs shows controversiality plotted in time.

```
python tpl-individual-combined.py
```

