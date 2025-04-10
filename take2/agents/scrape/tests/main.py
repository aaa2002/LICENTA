import json
import re
import requests
import nltk
from duckduckgo_search import DDGS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from nltk.tokenize import sent_tokenize

nltk.download('punkt')  # Needed for sentence splitting

# === LLaMA3: Query Helper ===
def query_ollama(prompt: str, model="llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        return f"[ERROR] {e}"

# === Step 1: Turn claim into question ===
def claim_to_question(claim: str):
    prompt = (
        # "You are an assistant that reformulates factual claims into factual questions.\n\n"
        "You are an assistant that reformulates claims into questions. W-questions are needed, i.e. questions which start with: Who, What, When, How.\n\n"
        "Respond ONLY with the question. Does not matter if it is disinformation.\n\n"
        f"Claim: \"{claim}\"\n"
        "Question:"
    )
    return query_ollama(prompt)

# === Step 2: DuckDuckGo Search ===
def get_search_results(query, num_results=5):
    with DDGS() as ddgs:
        return [r["body"] for r in ddgs.text(query, max_results=num_results)]

# === Step 3: Load REBEL for Relation Extraction ===
def load_re_model():
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    return tokenizer, model

# === Improved Relation Extraction ===
# === Improved Relation Extraction with LLM based on Entities ===
def extract_relations(text, tokenizer=None, model=None):
    import spacy
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    entities = [(ent.text, ent.label_) for ent in doc.ents]
    if not entities:
        return []

    prompt = (
        "You are an intelligent assistant that extracts factual relations in the form of triplets "
        "If you receive no entities, use the text to extract triplets directly.\n\n" # This was added later since in some cases spacy does not find any entities
        "(subject, relation, object) based on a given text and its named entities.\n\n"
        "Respond ONLY with a list of triplets in JSON format like this:\n"
        "[\n"
        "  [\"Barack Obama\", \"bornIn\", \"Hawaii\"],\n"
        "  [\"Trump\", \"presidentOf\", \"United States\"]\n"
        "]\n\n"
        f"Text: {text}\n\n"
        f"Named Entities: {entities}\n\n"
        "Triplets:"
    )

    result = query_ollama(prompt)

    try:
        return json.loads(result)
    except Exception:
        match = re.search(r"\[.*\]", result, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return []
        return []

# === Step 4: Send to LLM to Evaluate Graphs ===
def compare_graphs_llm(user_claim, user_triplets, web_triplets, model="llama3"):
    prompt = (
        "You are a reasoning agent that checks if a claim is factually correct based on extracted knowledge.\n\n"
        "ONLY respond in JSON format like this:\n"
        "{\n"
        "  \"supported\": true or false,\n"
        "  \"confidence\": float between 0 and 1,\n"
        "  \"explanation\": \"...\"\n"
        "}\n\n"
        f"User Claim: {user_claim}\n"
        f"Claim Triplets: {user_triplets}\n"
        f"Web Triplets: {web_triplets}\n"
        "Respond now:"
    )
    result = query_ollama(prompt, model=model)

    try:
        return json.loads(result)
    except Exception:
        match = re.search(r"\{.*\}", result, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return {"supported": None, "confidence": 0.0, "explanation": "Invalid JSON format in LLM response"}
        return {"supported": None, "confidence": 0.0, "explanation": "No JSON found in LLM response"}

# === MAIN PIPELINE ===
def main_pipeline(user_claim):
    print(f"[LOG] Claim: {user_claim}")

    # Step 1: Reformulate claim to a W-question
    question = claim_to_question(user_claim)
    print(f"[LOG] Reformulated question: {question}")

    # Step 2: Search the web
    web_results = get_search_results(question)
    web_text = " ".join(web_results)
    for i, res in enumerate(web_results):
        print(f"[LOG] Web Result {i+1}: {res[:150]}...")

    # Step 3: Extract relations
    tokenizer, model = load_re_model()
    print("[LOG] Extracting triplets...")
    user_rels = extract_relations(user_claim, tokenizer, model)
    web_rels = extract_relations(web_text, tokenizer, model)

    print(f"[LOG] Claim Relations: {user_rels}")
    print(f"[LOG] Web Relations: {web_rels[:5]}...")

    # Step 4: Verdict from LLM
    verdict = compare_graphs_llm(user_claim, user_rels, web_rels)
    print("\n[LOG] Verdict:")
    print(json.dumps(verdict, indent=2))

# === ENTRY POINT ===
if __name__ == "__main__":
    user_input = input("[LOG] Enter a news claim: ")
    main_pipeline(user_input)
