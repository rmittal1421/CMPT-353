import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

data =  pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

data2 =  pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

data = data.sort_values('views', ascending=False)

second_hour = pd.Series(
    data2['views'].values,
    index=data2.index
)

data['second_hour'] = second_hour

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) 
plt.plot(data['views'].values) 
plt.xlabel('Rank')
plt.ylabel('Views')
plt.title('Popularity Distribution')
plt.subplot(1, 2, 2) 
plt.plot(data['views'].values, data['second_hour'].values, 'b.')
plt.xlabel('Day 1 views')
plt.ylabel('Day 2 views')
plt.xscale('log')
plt.yscale('log')
plt.title('Daily Correlation')
plt.savefig('wikipedia.png')
