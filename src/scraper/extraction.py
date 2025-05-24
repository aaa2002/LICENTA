import json
import re
import spacy
from src.scraper.llm import query_ollama

def extract_relations(text, tokenizer=None, model=None):
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(text)

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    prompt = (
        "You are an intelligent assistant that extracts factual relations in the form of triplets. "
        "If you receive no entities, use the text to extract triplets directly.\n\n"
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
    if result.startswith("[ERROR]"):
        print("[ERROR] LLM request failed:", result)
        return []

    try:
        return json.loads(result)
    except Exception:
        match = re.search(r"\[.*?\]", result, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return []
        return []