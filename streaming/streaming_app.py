from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder \
    .appName("KafkaStreamingApp") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("ip", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("method", StringType(), True),
    StructField("url", StringType(), True),
    StructField("status_code", IntegerType(), True),
    StructField("response_size", IntegerType(), True),
    StructField("user_agent", StringType(), True)
])

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "web_logs") \
    .option("startingOffsets", "earliest") \
    .load()

raw_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str")

parsed_df = raw_df \
    .select(
        col("json_str"),
        from_json(col("json_str"), schema).alias("data")
    ) \
    .select(
        col("json_str"),
        col("data.ip").alias("ip"),
        col("data.timestamp").alias("timestamp"),
        col("data.method").alias("method"),
        col("data.url").alias("url"),
        col("data.status_code").alias("status_code"),
        col("data.response_size").alias("response_size"),
        col("data.user_agent").alias("user_agent")
    )

typed_df = parsed_df.withColumn(
    "event_time",
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

clean_df = typed_df.filter(
    col("ip").isNotNull() &
    col("event_time").isNotNull() &
    col("method").isNotNull() &
    col("url").isNotNull() &
    col("status_code").isNotNull() &
    col("response_size").isNotNull() &
    (col("status_code") >= 100) &
    (col("status_code") <= 599) &
    (col("response_size") >= 0)
)

query = clean_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
