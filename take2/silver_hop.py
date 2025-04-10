import spacy
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from delta import configure_spark_with_delta_pip

# -------------------------------
# Spark Session with Delta Config
# -------------------------------
builder = SparkSession.builder \
    .appName("Cleaned Silver Table") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# -------------------
# Load spaCy model
# -------------------
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])  # Faster without NER/parser

# -------------------
# Text cleaning UDF
# -------------------
def clean_text(text):
    if text is None:
        return ""

    text = re.sub(r'\s+', ' ', text)              # Normalize whitespace
    text = re.sub(r'\d+', '', text)               # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)           # Remove punctuation
    text = text.lower().strip()                   # Lowercase

    doc = nlp(text)

    tokens = [
        token.lemma_ for token in doc
        if token.lemma_ != '-PRON-' and not token.is_stop and token.is_alpha
    ]

    return ' '.join(tokens)

# Register as Spark UDF
clean_text_udf = udf(clean_text, StringType())

# ---------------------
# Load Bronze Table
# ---------------------
df_bronze = spark.read.format("delta").load("./delta/all_news")

# ---------------------
# Apply Cleaning
# ---------------------
df_silver = df_bronze.withColumn("clean_text", clean_text_udf(df_bronze.text))

# ---------------------
# Save Silver Table
# ---------------------
df_silver.write.format("delta").mode("overwrite").save("./delta/silver_cleaned_news")

# Optional: Register SQL table
spark.sql("CREATE TABLE IF NOT EXISTS silver_cleaned_news USING DELTA LOCATION './delta/silver_cleaned_news'")

# Preview cleaned data
df_silver.select("truth", "clean_text").show(5, truncate=False)
