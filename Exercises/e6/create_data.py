import numpy as np
import pandas as pd
import time
from implementations import all_implementations

data = pd.DataFrame()

for sort in all_implementations:
    times_for_sort = np.array([], dtype=float)
    for iter in range(50):
        random_array = np.random.randint(100000, size=10000)
        st = time.time()
        res = sort(random_array)
        en = time.time()
        times_for_sort = np.append(times_for_sort, en - st)
    data[sort.__name__] = times_for_sort

data.to_csv('data.csv', index=False)