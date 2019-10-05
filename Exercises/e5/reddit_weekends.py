import sys
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

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

def get_iso_year(date):
    return date.isocalendar()[0]

def get_iso_week(date):
    return date.isocalendar()[1]

def main():
    reddit_counts = sys.argv[1]
    counts = pd.read_json(reddit_counts, lines=True)
    counts = counts[((counts['date'].dt.year == 2012) | (counts['date'].dt.year == 2013)) & (counts['subreddit'] == 'canada')]
    counts['iso_year'] = counts['date'].apply(get_iso_year)
    counts['iso_week'] = counts['date'].apply(get_iso_week)

    weekdays = counts[(counts['date'].dt.weekday != 5) & (counts['date'].dt.weekday != 6)]
    weekends = counts[(counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6)]

    unalt_comment_count_weekdays = weekdays['comment_count']
    unalt_comment_count_weekends = weekends['comment_count']

    initial_ttest_p_value = stats.ttest_ind(unalt_comment_count_weekdays, unalt_comment_count_weekends).pvalue
    initial_weekday_normality_p_value = stats.normaltest(unalt_comment_count_weekdays).pvalue
    initial_weekend_normality_p_value = stats.normaltest(unalt_comment_count_weekends).pvalue
    initial_levene_p_value = stats.levene(unalt_comment_count_weekdays, unalt_comment_count_weekends).pvalue

    comment_count_weekdays = np.sqrt(unalt_comment_count_weekdays)
    comment_count_weekends = np.sqrt(unalt_comment_count_weekends)

    transformed_weekday_normality_p_value = stats.normaltest(comment_count_weekdays).pvalue
    transformed_weekend_normality_p_value = stats.normaltest(comment_count_weekends).pvalue
    transformed_levene_p_value = stats.levene(comment_count_weekdays, comment_count_weekends).pvalue

    weekdays = weekdays.groupby(['iso_year', 'iso_week']).aggregate('mean').reset_index()
    weekends = weekends.groupby(['iso_year', 'iso_week']).aggregate('mean').reset_index()

    comment_count_weekdays = weekdays['comment_count']
    comment_count_weekends = weekends['comment_count']

    weekly_weekday_normality_p_value = stats.normaltest(comment_count_weekdays).pvalue
    weekly_weekend_normality_p_value = stats.normaltest(comment_count_weekends).pvalue
    weekly_levene_p_value = stats.levene(comment_count_weekdays, comment_count_weekends).pvalue
    weekly_ttest_p_value = stats.ttest_ind(comment_count_weekdays, comment_count_weekends).pvalue
    
    utest_p_value = stats.mannwhitneyu(unalt_comment_count_weekdays, unalt_comment_count_weekends, alternative='two-sided').pvalue

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p_value,
        initial_weekday_normality_p=initial_weekday_normality_p_value,
        initial_weekend_normality_p=initial_weekend_normality_p_value,
        initial_levene_p=initial_levene_p_value,
        transformed_weekday_normality_p=transformed_weekday_normality_p_value,
        transformed_weekend_normality_p=transformed_weekend_normality_p_value,
        transformed_levene_p=transformed_levene_p_value,
        weekly_weekday_normality_p=weekly_weekday_normality_p_value,
        weekly_weekend_normality_p=weekly_weekend_normality_p_value,
        weekly_levene_p=weekly_levene_p_value,
        weekly_ttest_p=weekly_ttest_p_value,
        utest_p=utest_p_value,
    ))


if __name__ == '__main__':
    main()