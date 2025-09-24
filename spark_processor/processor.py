from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, DoubleType
from textblob import TextBlob

# Spark Session
spark = SparkSession.builder \
    .appName("RedditSentimentAnalysis") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# Kafka Source
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "reddit_posts") \
    .load()

# Schema for Reddit data
schema = StructType() \
    .add("id", StringType()) \
    .add("title", StringType()) \
    .add("subreddit", StringType()) \
    .add("created_utc", StringType()) \
    .add("url", StringType())

# Parse JSON
json_df = df.selectExpr("CAST(value AS STRING)")
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Sentiment Analysis UDF
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

sentiment_udf = udf(get_sentiment, DoubleType())

with_sentiment = parsed_df.withColumn("sentiment", sentiment_udf(col("title")))

# Write to PostgreSQL
query = with_sentiment.writeStream \
    .foreachBatch(lambda batch_df, _: batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/redditdb") \
        .option("dbtable", "reddit_posts") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .mode("append") \
        .save()) \
    .outputMode("update") \
    .start()

query.awaitTermination()
