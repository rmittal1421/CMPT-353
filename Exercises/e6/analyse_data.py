import numpy as np
import pandas as pd
from scipy import stats
from implementations import all_implementations
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from matplotlib import pyplot as plt 

df = pd.read_csv('data.csv')
rankings = []

test = stats.f_oneway(df.qs1, df.qs2, df.qs3, df.qs4, df.qs5, df.merge1, df.partition_sort)

df = df.melt()
# print(df)
fig,ax = plt.subplots()
posthoc = pairwise_tukeyhsd(
    df['value'], df['variable'],
    alpha=0.05)

posthoc.plot_simultaneous(ax=ax)


