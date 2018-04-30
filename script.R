rm(list=ls())

library('leaps')

dat = read.csv('notebooks/data.csv')
head(dat)

null = glm(controversial ~ 1, data=dat, family='binomial')
full = glm(controversial ~ . - X - name - screen_name - industry, 
           data=dat, family='binomial')

step(null, scope=list(lower=null, upper=full), direction="both")

best = glm(formula = controversial ~ polarity + favorite_count_about, 
           data=dat, family="binomial")
summary(best)

