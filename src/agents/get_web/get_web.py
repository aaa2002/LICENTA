from src.scraper.search import get_search_results
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
import uuid
import json
from src.scraper.llm import query_ollama

def get_top_k_results_delta(question, k=5):
    delta_path = "src/delta/web_results"

    # Step 1: Start Spark with Delta config
    spark = (
        SparkSession.builder
        .appName("WebResultsToDelta")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

    # Step 2: Read existing questions (with fallback if DeltaTable fails)
    existing_records = []
    try:
        if DeltaTable.isDeltaTable(spark, delta_path):
            df_existing = spark.read.format("delta").load(delta_path).select("id", "question", "web_results_json")
            existing_records = df_existing.toPandas().to_dict(orient="records")
    except Exception as e:
        print(f"[WARN] Skipping DeltaTable check: {e}")
        existing_records = []

    # Step 3: Use LLM to check for fuzzy match
    prompt = "The following is a list of questions and their IDs:\n\n"
    for r in existing_records:
        prompt += f"ID: {r['id']}\nQuestion: {r['question']}\n\n"

    prompt += (
        f"This is a new question:\n{question}\n\n"
        "Does this question convey the same meaning as any of the others?\n"
        "If so, return {\"id\": <ID of the matching question>}.\n"
        "Else, return {\"id\": \"None\"}.\n"
        "Respond ONLY with the JSON object.\n"
    )

    print(f"[LOG] LLM Prompt: {prompt[:500]}...")
    print(f"prompt: {prompt}")
    matched_id = json.loads(query_ollama(prompt))['id']

    # Step 4: If match found, return existing result
    if matched_id and matched_id != "None":
        print(f"[Info] Matched existing question with ID: {matched_id}")
        match = next((r for r in existing_records if str(r["id"]) == str(matched_id)), None)
        if match:
            return [match["web_results_json"]], match["web_results_json"]
    print(spark.version)

    # Step 5: Perform fresh search and store it
    web_results = get_search_results(question["text"], k)
    web_text = " ".join(web_results)

    new_id = str(uuid.uuid4())
    df = spark.createDataFrame([{
        "id": new_id,
        "question": question,
        "web_results_json": web_text
    }])
    df.write.format("delta").mode("append").save(delta_path)

    for i, res in enumerate(web_results):
        print(f"[LOG] Web Result {i + 1}: {res[:150]}...")

    return web_results, web_text
