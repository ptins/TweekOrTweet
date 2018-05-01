rm(list=ls())

library('leaps')

dat = read.csv('trial.csv')
head(dat)



null = glm(controversial ~ 1, data=dat, family='binomial')
full = glm(controversial ~ favorite_count + retweet_count + polarity, 
           data=dat, family='binomial')

step(null, scope=list(lower=null, upper=full), direction="both")

best = glm(formula = controversial ~ polarity + favorite_count, 
           data=dat, family="binomial")
summary(best)

