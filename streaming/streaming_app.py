from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Создаем SparkSession
spark = SparkSession.builder \
    .appName("KafkaStreamingApp") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Схема для JSON
schema = StructType([
    StructField("ip", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("method", StringType(), True),
    StructField("url", StringType(), True),
    StructField("status_code", IntegerType(), True),
    StructField("response_size", IntegerType(), True),
    StructField("user_agent", StringType(), True)
])

# Чтение из Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "web_logs") \
    .option("startingOffsets", "earliest") \
    .load()

# Конвертация значения из Kafka из bytes в строку и парсинг JSON
json_df = df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Вывод в консоль
query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
