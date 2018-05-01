rm(list=ls())

library('leaps')

df_about = read.csv('user_tweets_about.csv')
head(df_about)

df_people = read.csv('people_list.csv')
head(df_people)

dat = merge(df_about, df_people)
head(dat)

null = glm(controversial ~ 1, data=dat, family='binomial')
full = glm(controversial ~ favorite_count + retweet_count + polarity, 
           data=dat, family='binomial')

step(null, scope=list(lower=null, upper=full), direction="both")

best = glm(formula = controversial ~ polarity + retweet_count, 
           data=dat, family="binomial")
summary(best)

