from src.scraper.llm import claim_to_question, compare_graphs_llm
from src.scraper.extraction import extract_relations
from src.agents.scrape.utils import load_re_model
from src.agents.get_web.get_web import get_top_k_results_delta
import json

def main_pipeline(user_claim, web_text=None, logging=True):
    print(f"[LOG] --- [pipeline.py] - Claim: {user_claim}")

    # Extract relations
    tokenizer, model = load_re_model()
    print("[LOG] --- [pipeline.py] - Extracting triplets...")
    user_rels = extract_relations(user_claim, tokenizer, model)
    web_rels = extract_relations(web_text, tokenizer, model)

    print(f"[LOG] --- [pipeline.py] - Claim Relations: {user_rels}")
    print(f"[LOG] --- [pipeline.py] - Web Relations: {web_rels[:5]}...")

    # Verdict from LLM
    try:
        verdict = compare_graphs_llm(user_claim, user_rels, web_rels)
    except Exception as e:
        print(f"[ERROR] --- [pipeline.py] - LLM comparison failed: {e}")
        return {"label": None, "confidence": 0.0, "explanation": "LLM comparison failed"}

    if logging:
        print("\n[LOG] --- [pipeline.py] - Verdict:")
        print(json.dumps(verdict, indent=2))

    return verdict
