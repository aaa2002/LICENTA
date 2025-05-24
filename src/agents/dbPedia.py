import spacy
import wikipedia
from SPARQLWrapper import SPARQLWrapper, JSON
from take2.scraper.llm import query_ollama
import re

class DbPediaAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    def llama_generate_sparql(self, term):
        prompt = (
            f"You are a SPARQL expert. Generate a SPARQL query to retrieve the English abstract from DBpedia "
            f"for the entity '{term}'. Return only the SPARQL query, no explanations, no formatting, no ``` blocks."
        )
        raw = query_ollama(prompt).strip()

        # Remove markdown/code blocks
        if raw.startswith("```"):
            raw = raw.strip("`").strip()

        # Remove any prefixed explanations
        raw = re.sub(r"(?i)^here is the sparql query:.*?\n", "", raw).strip()

        # Fix malformed FILTER clause
        raw = raw.replace('FILTER lang(', 'FILTER (lang(')
        raw = raw.replace('FILTER (lang(?abstract) = "en" .', 'FILTER (lang(?abstract) = "en") .')
        raw = raw.replace('FILTER (lang(?abs) = "en" .', 'FILTER (lang(?abs) = "en") .')

        # Ensure query ends with properly balanced braces
        if raw.count("{") > raw.count("}"):
            raw += " }" * (raw.count("{") - raw.count("}"))

        return raw

    def search_dbpedia(self, term):
        try:
            query = self.llama_generate_sparql(term)
            if not query.lower().startswith("select"):
                raise ValueError("Generated query is not a SELECT SPARQL")
        except Exception as e:
            print(f"[LLaMA3 SPARQL ERROR] {e}")
            query = f"""
            SELECT ?abstract WHERE {{
                ?entity rdfs:label "{term}"@en .
                ?entity dbo:abstract ?abstract .
                FILTER (lang(?abstract) = 'en')
            }}
            LIMIT 1
            """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

        try:
            results = self.sparql.query().convert()
            bindings = results.get("results", {}).get("bindings", [])
            if bindings:
                return bindings[0]["abstract"]["value"]
        except Exception as e:
            print(f"[DBpedia ERROR] {e}")
        return ""

    def search_wikipedia(self, term):
        abstract = self.search_dbpedia(term)
        if abstract:
            return abstract

        try:
            results = wikipedia.search(term)
            if not results:
                return ""
            if len(results) == 1:
                return wikipedia.summary(results[0], sentences=3)
            # Try direct match
            try:
                return wikipedia.summary(term, sentences=3)
            except wikipedia.DisambiguationError:
                print(f"[Wikipedia WARNING] Ambiguous term '{term}', skipping.")
        except Exception as e:
            print(f"[Wikipedia ERROR] {e}")
        return ""

    def keyword_overlap(self, text1, text2):
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        keywords1 = {token.lemma_ for token in doc1 if token.pos_ in ['NOUN', 'PROPN', 'VERB']}
        keywords2 = {token.lemma_ for token in doc2 if token.pos_ in ['NOUN', 'PROPN', 'VERB']}
        overlap = keywords1 & keywords2
        return len(overlap) / max(len(keywords1), 1)

    def extract_search_terms(self, text):
        doc = self.nlp(text)
        candidates = set()

        for ent in doc.ents:
            if ent.label_ in ("PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART"):
                candidates.add(ent.text.strip())

        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                candidates.add(chunk.text.strip())

        for token in doc:
            if token.pos_ in ("NOUN", "PROPN") and token.dep_ in ("nsubj", "dobj", "attr", "ROOT"):
                if len(token.text) > 2 and token.is_alpha:
                    candidates.add(token.text.strip())

        cleaned = {term.title() for term in candidates if term.isascii()}
        return list(cleaned)

    def analyze(self, text):
        search_terms = self.extract_search_terms(text)
        print("Search terms:", search_terms)

        wiki_facts = " ".join([self.search_wikipedia(term) for term in search_terms])

        if not wiki_facts.strip():
            return {
                'label': 'FAKE',
                'confidence': 0.9,
                'overlap_score': 0.0,
                'search_terms': search_terms,
                'evidence': ''
            }

        score = self.keyword_overlap(text, wiki_facts)
        confidence = round(1.0 - score, 3)
        label = 'FAKE' if confidence > 0.5 else 'REAL'

        return {
            'label': label,
            'confidence': confidence,
            'overlap_score': round(score, 3),
            'search_terms': search_terms,
            'evidence': wiki_facts[:500] + "..." if len(wiki_facts) > 500 else wiki_facts
        }
