import sys
import numpy as np
import pandas as pd

filename = sys.argv[1]

data = pd.read_csv(filename, sep=',', header=None, index_col=1,
        names=['cpu_freq', 'cpu_percent', 'sys_load_1', 'temperature', 'timestamp'])

print(data)