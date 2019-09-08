import numpy as np
import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

# 1st question
sum = totals.sum(axis=1)
print('City with lowest total precipitation:')
print(sum.idxmin())

# 2nd question
sum_monthWise = totals.sum(axis=0)
sum_count_monthWise = counts.sum(axis=0)
average = sum_monthWise/sum_count_monthWise
print('Average precipitation in each month:')
print(average)

# 3rd question
total_cityWise = totals.sum(axis=1)
total_count_cityWise = counts.sum(axis = 1)
average_city = total_cityWise/total_count_cityWise
print('Average precipitation in each city:')
print(average_city)



