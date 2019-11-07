import numpy as np
from scipy import stats


def run_experiment(n: int) -> float:
    x = np.random.normal(0, 1, n)
    y = np.random.normal(0, 1, n)
    ttest = stats.ttest_ind(x, y)
    return ttest.pvalue


alpha = 0.05
experiments = 20
n = 100

for i in range(experiments):
    p = run_experiment(n)
    if p < alpha/experiments:
        print(p, '!!! "significant with Bonferroni correction"')
    elif p < alpha:
        print(p, '*** "significant"')
    else:
        print(p)
