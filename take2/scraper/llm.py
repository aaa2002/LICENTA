import json
import re
import requests

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
        "You are an assistant that reformulates claims into questions. W-questions are needed, i.e. questions which start with: Who, What, When, How.\n\n"
        "Respond ONLY with the question. Does not matter if it is disinformation.\n\n"
        f"Claim: \"{claim}\"\n"
        "Question:"
    )
    return query_ollama(prompt)

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