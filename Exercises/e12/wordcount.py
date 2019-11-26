import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import numpy as np
import pandas as pd
import string

spark = SparkSession.builder.appName('word count').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation

def main(in_directory, out_directory):
    words = spark.read.text(in_directory)
    words = words.select(functions.explode(functions.split(words['value'], wordbreak)).alias('word'))
    words = words.select(functions.lower(words['word']).alias('word'))
    words = words.groupBy(words.word).agg(functions.count(functions.lit(1)).alias('count'))
    words = words.orderBy(['count', 'word'], ascending=[0, 1])
    words = words.filter(words['word'] != '')
    words.show()
    words.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)