from src.scraper.search import get_search_results
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
import uuid
import json
from src.scraper.llm import query_ollama
from datetime import date

def get_top_k_results_delta(question, k=5):
    delta_path = "src/delta/web_results"

    spark = (
        SparkSession.builder
        .appName("WebResultsToDelta")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

    existing_records = []
    try:
        if DeltaTable.isDeltaTable(spark, delta_path):
            df_existing = spark.read.format("delta").load(delta_path).select("id", "question", "web_results_json")
            existing_records = df_existing.toPandas().to_dict(orient="records")
    except Exception as e:
        print(f"[LOG] --- [get_web.py] - Skipping DeltaTable check: {e}")
        existing_records = []

    prompt = "The following is a list of questions and their IDs:\n\n"
    for r in existing_records:
        prompt += f"ID: None\nQuestion: {r['question']}\n\n"
        # prompt += f"ID: {r['id']}\nQuestion: {r['question']}\n\n"

    prompt += (
        f"This is a new question:\n{question}\n\n"
        # "Does this question talk about the same topic as any of the others?\n"
        # "There might be no matching options, highly probable even.\n"
        # "Negative answers are also valid and important.\n"
        "return {\"id\": \"None\"}\n"
        # "If it does not match the same meaning, return {\"id\": \"None\"}\n"
        # "Else, return {\"id\": <ID of the matching question>}.\n"
        "Respond ONLY with the JSON object.\n"
    )

    print(f"[LOG] --- [get_web.py] - Prompt: \n\n{prompt}\n\n")
    matched_id = json.loads(query_ollama(prompt))['id']

    if matched_id and matched_id != "None":
        print(f"[LOG] --- [get_web.py] - Matched existing question with ID: {matched_id}")
        match = next((r for r in existing_records if str(r["id"]) == str(matched_id)), None)
        if match:
            return [match["web_results_json"]], match["web_results_json"]
    print("[LOG] --- [get_web.py] - " + spark.version)

    try:
        today_str = date.today().strftime("%Y-%m-%d")
        web_results = get_search_results(question + f"\n\n Date {today_str}", k)
        web_text = " ".join(web_results)
    except Exception as e:
        print(f"[LOG] --- [get_web.py] - Search failed: {e}")
        return [], ""

    new_id = str(uuid.uuid4())
    try:
        df = spark.createDataFrame([{
            "id": new_id,
            "question": {"text": question},
            "web_results_json": web_text
        }])
        df.write.format("delta").mode("append").save(delta_path)
    except Exception as e:
        print(f"[LOG] --- [get_web.py] - Failed to write to Delta: {e}")
        return [], ""

    for i, res in enumerate(web_results):
        print(f"[LOG] --- [get_web.py] - Web Result {i + 1}: {res[:150]}...")

    return web_results, web_text
