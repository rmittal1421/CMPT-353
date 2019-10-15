import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv('data.csv')
test = stats.f_oneway(df.qs1, df.qs2, df.qs3, df.qs4, df.qs5, df.merge1, df.partition_sort)
print(test.pvalue)

df = df.melt()
posthoc = pairwise_tukeyhsd(
    df['value'], df['variable'],
    alpha=0.05)

print(posthoc)


