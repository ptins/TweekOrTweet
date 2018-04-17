data = read.csv('notebooks/data.csv')
head(data)

fit = glm(controversial ~ . - X - name - screen_name - industry, data = data)
summary(fit)

library(MASS)
fit = glm(controversial ~ . - X - name - screen_name - industry, data = data)
step <- stepAIC(fit, direction="both")
