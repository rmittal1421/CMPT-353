import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('Wikipedia visits').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wiki_data_schema = types.StructType([
    types.StructField('lan', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('count', types.LongType()),
    types.StructField('bytes', types.LongType()),
])

def path_to_hour_non_udf(names):
    split_string = names.split('-')
    return split_string[-2] + '-' + split_string[-1][:2]

def main(in_directory, out_directory):
    path_to_hour = functions.udf(path_to_hour_non_udf, returnType=types.StringType())

    stats = spark.read.csv(in_directory, schema=wiki_data_schema, sep=' ').withColumn('filename', path_to_hour(functions.input_file_name()))
    stats = stats.filter((stats['lan'] == 'en') & (stats['name'] != 'Main_Page') & ~(stats['name'].startswith('Special:'))).cache() # <------ Caching here!

    max_stats = stats.groupBy('filename').agg(functions.max('count')).alias('max(count)')

    stats = max_stats.join(stats, on='filename')

    # stats.explain()
    stats = stats.filter(stats['max(count)'] == stats['count'])

    stats_sorted = stats.sort('filename', 'name')
    cleaned_data = stats_sorted.select(
        stats_sorted['filename'],
        stats_sorted['name'],
        stats_sorted['count']
    )
    cleaned_data.write.csv(out_directory, mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)