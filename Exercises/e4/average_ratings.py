import sys
import numpy as np
import pandas as pd
import re
import difflib

movies = sys.argv[1] # input file actual movie names
rating = sys.argv[2] # input file of the reviews given by the viewers
ratingDf = pd.read_csv(rating) # DataFrame to store the ratings given by the viewers

# Following function has been adapted from https://stackoverflow.com/questions/275018/how-can-i-remove-a-trailing-newline
def removeTailingNewLine(line):
    if re.search("(\\r|)\\n$", line):
        return re.sub("(\\r|)\\n$", "", line)

some = pd.Series(open(movies).readlines()).apply(removeTailingNewLine)

df = pd.DataFrame({
    'title': some,
})

def findClosestTitle(movie):
    matching_titles = difflib.get_close_matches(movie, df['title'])
    if (len(matching_titles) > 0):
        return matching_titles[0]
    return ""

ratingDf['title'] = ratingDf['title'].apply(findClosestTitle)
ratingDf = ratingDf[ratingDf.title != ""]
ratingDf = ratingDf.groupby(['title']).aggregate('mean').reset_index().round(2)
ratingDf.to_csv(sys.argv[3], index=False)