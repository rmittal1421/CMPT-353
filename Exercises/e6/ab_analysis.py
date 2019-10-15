import sys
import numpy as np
import pandas as pd
from scipy import stats

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    df = pd.read_json(searchdata_file, orient='records', lines=True)
    odd_users = df[df['uid']%2 != 0]
    even_users = df[df['uid']%2 == 0]

    never_searched_odd = odd_users[odd_users['search_count'] == 0]
    never_searched_even = even_users[even_users['search_count'] == 0]
    searched_odd = odd_users[odd_users['search_count'] != 0]
    searched_even = even_users[even_users['search_count'] != 0]    
    contingency1 = [[len(searched_even), len(never_searched_even)], [len(searched_odd), len(never_searched_odd)]]

    never_searched_instr_odd = odd_users[(odd_users['search_count'] == 0) & (odd_users['is_instructor'] == True)]
    never_searched_instr_even = even_users[(even_users['search_count'] == 0) & (even_users['is_instructor'] == True)]
    searched__instr_odd = odd_users[(odd_users['search_count'] != 0) & (odd_users['is_instructor'] == True)]
    searched_instr_even = even_users[(even_users['search_count'] != 0) & (even_users['is_instructor'] == True)]
    contingency2 = [[len(searched_instr_even), len(never_searched_instr_even)], [len(searched__instr_odd), len(never_searched_instr_odd)]]

    more_users_p_value = stats.chi2_contingency(contingency1)[1]
    more_searches_p_value = stats.mannwhitneyu(even_users['search_count'], odd_users['search_count'], alternative='two-sided').pvalue
    more_instr_p_value = stats.chi2_contingency(contingency2)[1]
    more_instr_searches_p = stats.mannwhitneyu(odd_users[odd_users['is_instructor']]['search_count'], even_users[even_users['is_instructor']]['search_count'], alternative='two-sided').pvalue

    # ...

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=more_users_p_value,
        more_searches_p=more_searches_p_value,
        more_instr_p=more_instr_p_value,
        more_instr_searches_p=more_instr_searches_p,
    ))


if __name__ == '__main__':
    main()