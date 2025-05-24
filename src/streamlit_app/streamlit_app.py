import streamlit as st
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder \
    .appName("Delta Viewer") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

df = spark.read.format("delta").load("../delta/silver_cleaned_news")

pandas_df = df.toPandas()

st.title("Delta Table Viewer")
st.dataframe(pandas_df.head(40000))
