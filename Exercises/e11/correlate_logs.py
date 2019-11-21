import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import numpy as np
import pandas as pd
from pprint import pprint
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        _, hostname, bytes_transferred, _ = re.split(line_re, line)
        return Row(hostname=hostname, bytes_transferred=int(bytes_transferred))
    else:
        return None

def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    return log_lines.map(line_to_row).filter(not_none)

def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    logs = logs.groupBy(logs.hostname).agg(functions.count(functions.lit(1)).alias('count_requests'), functions.sum(logs.bytes_transferred).alias('sum_request_bytes'))
    sums = logs.select(
        functions.lit(1),
        logs.count_requests,
        logs.sum_request_bytes,
        logs.count_requests ** 2,
        logs.sum_request_bytes ** 2,
        logs.count_requests * logs.sum_request_bytes
    ).groupBy().sum()

    n, sum_x, sum_y, sum_x_sq, sum_y_sq, sum_xy = sums.first()

    r = (n*sum_xy - sum_x*sum_y)/(math.sqrt(n*sum_x_sq - sum_x ** 2)*math.sqrt(n*sum_y_sq - sum_y ** 2))
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
