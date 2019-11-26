import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import numpy as np
import pandas as pd
import string, re

spark = SparkSession.builder.appName('word count').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
compiled_re = re.compile(wordbreak)

def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    return re.split(compiled_re, line)

def main(in_directory, out_directory):
    lines =  spark.read.text(in_directory)
    df = lines.select(functions.explode(functions.split(lines['value'], wordbreak)).alias('word'))
    df = df.select(functions.lower(df['word']).alias('word'))
    df = df.groupBy(df.word).agg(functions.count(functions.lit(1)).alias('count'))
    df = df.orderBy(['count', 'word'], ascending=[0, 1])
    df = df.filter(df['word'] != '')
    df.show()
    # df.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)