import spacy
from typing import List, Dict
from src.agents.queryGen.query_dataset_generator import generate_query

class QueryGenerator:
    def __init__(self, min_entity_len=3, mode='auto'):
        self.min_entity_len = min_entity_len
        self.mode = mode
        self.nlp = spacy.load("en_core_web_sm")

    def generate(self, raw_text: str) -> Dict[str, str]:
        return generate_query(raw_text)
