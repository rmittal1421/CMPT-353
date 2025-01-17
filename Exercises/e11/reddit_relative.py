import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

schema = types.StructType([ # commented-out fields won't be read
    #types.StructField('archived', types.BooleanType(), False),
    types.StructField('author', types.StringType(), False),
    #types.StructField('author_flair_css_class', types.StringType(), False),
    #types.StructField('author_flair_text', types.StringType(), False),
    #types.StructField('body', types.StringType(), False),
    #types.StructField('controversiality', types.LongType(), False),
    #types.StructField('created_utc', types.StringType(), False),
    #types.StructField('distinguished', types.StringType(), False),
    #types.StructField('downs', types.LongType(), False),
    #types.StructField('edited', types.StringType(), False),
    #types.StructField('gilded', types.LongType(), False),
    #types.StructField('id', types.StringType(), False),
    #types.StructField('link_id', types.StringType(), False),
    #types.StructField('name', types.StringType(), False),
    #types.StructField('parent_id', types.StringType(), True),
    #types.StructField('retrieved_on', types.LongType(), False),
    types.StructField('score', types.LongType(), False),
    #types.StructField('score_hidden', types.BooleanType(), False),
    types.StructField('subreddit', types.StringType(), False),
    #types.StructField('subreddit_id', types.StringType(), False),
    #types.StructField('ups', types.LongType(), False),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=schema).cache()

    averages = comments.groupBy('subreddit').agg(functions.avg(comments['score']).alias('avg_score'))
    averages = averages.filter(averages.avg_score > 0)

    # comments = comments.join(averages, on='subreddit') # -- without broadcast
    comments = comments.join(functions.broadcast(averages), on='subreddit') # -- with broadcast
    comments = comments.withColumn('rel_score', comments.score/comments.avg_score).cache()
    max_relative = comments.groupBy('subreddit').agg(functions.max(comments['rel_score']).alias('max_rel_score'))
    # comments = comments.join(max_relative, on='subreddit')  # -- without broadcast
    comments = comments.join(functions.broadcast(max_relative), on='subreddit')  # -- with broadcast
    comments = comments.filter(comments['max_rel_score'] == comments['rel_score'])

    best_author = comments.select(
        comments['subreddit'],
        comments['author'],
        comments['rel_score']
    )

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
