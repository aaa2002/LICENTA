from take2.agents.scrape.llm import claim_to_question, compare_graphs_llm
from take2.agents.scrape.search import get_search_results
from take2.agents.scrape.extraction import extract_relations
from take2.agents.scrape.utils import load_re_model
import json

# === MAIN PIPELINE ===
def main_pipeline(user_claim, logging = True):
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
    if logging:
        print("\n[LOG] Verdict:")
        print(json.dumps(verdict, indent=2))

    return verdict