import numpy as np
import pandas as pd
from datetime import date
import sys


OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]
    counts = pd.read_json(reddit_counts, lines=True)
    counts = counts[((counts['date'].dt.year == 2012) | (counts['date'].dt.year == 2013)) & (counts['subreddit'] == 'canada')]
    # print(len(counts))

    weekends = counts[(counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6)]
    weekdays = counts[(counts['date'].dt.weekday != 5) & (counts['date'].dt.weekday != 6)]

    print(weekends)
    # ...

    # print(OUTPUT_TEMPLATE.format(
    #     initial_ttest_p=0,
    #     initial_weekday_normality_p=0,
    #     initial_weekend_normality_p=0,
    #     initial_levene_p=0,
    #     transformed_weekday_normality_p=0,
    #     transformed_weekend_normality_p=0,
    #     transformed_levene_p=0,
    #     weekly_weekday_normality_p=0,
    #     weekly_weekend_normality_p=0,
    #     weekly_levene_p=0,
    #     weekly_ttest_p=0,
    #     utest_p=0,
    # ))


if __name__ == '__main__':
    main()