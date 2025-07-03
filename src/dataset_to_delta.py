from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import lit

builder = SparkSession.builder \
    .appName("CSV to Delta Table") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

schema = StructType([
    StructField("text", StringType(), True),
    StructField("truth", IntegerType(), True)
])

read_options = {
    "header": True,
    "schema": schema,
    "multiLine": True,
    "quote": '"',
    "escape": '"'
}

df_fake = spark.read.options(**read_options).csv('./filtered/filtered_fake.csv')
df_real = spark.read.options(**read_options).csv('./filtered/filtered_real.csv')

if df_fake.filter("truth IS NOT NULL").count() == 0:
    df_fake = df_fake.drop("truth").withColumn("truth", lit(0))
if df_real.filter("truth IS NOT NULL").count() == 0:
    df_real = df_real.drop("truth").withColumn("truth", lit(1))

df_fake.write.format("delta").mode("overwrite").save("./delta/fake_news")
df_real.write.format("delta").mode("overwrite").save("./delta/real_news")

df_combined = df_fake.union(df_real)
df_combined.write.format("delta").mode("overwrite").save("./delta/all_news")
