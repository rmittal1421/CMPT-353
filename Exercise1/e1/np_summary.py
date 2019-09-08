import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

# 1st question
sum = np.sum(totals, axis = 1)
minimum_total_prec = np.argmin(sum)
print('Row with lowest total precipitation:')
print(minimum_total_prec)

# 2nd question
total_monthWise = np.sum(totals, axis = 0)
total_count = np.sum(counts, axis = 0)
average = total_monthWise/total_count
print('Average precipitation in each month:')
print(average)

# 3rd question
total_cityWise = np.sum(totals, axis = 1)
total_count_cityWise = np.sum(counts, axis = 1)
average_city = total_cityWise/total_count_cityWise
print('Average precipitation in each city:')
print(average_city)

# 4th question
new_totals = totals.reshape(len(totals), 4, 3)
total_quaterly = np.sum(new_totals, axis = 2)
print('Quarterly precipitation totals:')
print(total_quaterly)

