import spacy
import wikipedia

class WikiAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def search_wikipedia(self, term):
        try:
            results = wikipedia.search(term)
            if results:
                return wikipedia.summary(results[0], sentences=3)
            return ""
        except Exception:
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

        # Named entities that are likely to have wiki pages
        for ent in doc.ents:
            if ent.label_ in ("PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART"):
                candidates.add(ent.text.strip())

        # Noun chunks (multi-word phrases)
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                candidates.add(chunk.text.strip())

        # Also include important standalone nouns and subjects
        for token in doc:
            if token.pos_ in ("NOUN", "PROPN") and token.dep_ in ("nsubj", "dobj", "attr", "ROOT"):
                if len(token.text) > 2 and token.is_alpha:
                    candidates.add(token.text.strip())

        # Clean and normalize
        cleaned = {term.title() for term in candidates if term.isascii()}
        return list(cleaned)

    def analyze(self, text):
        search_terms = self.extract_search_terms(text)
        print("Wikipedia search terms:", search_terms)

        wiki_facts = " ".join([self.search_wikipedia(term) for term in search_terms])

        if not wiki_facts.strip():
            return {'label': 'fake', 'confidence': 0.9}

        score = self.keyword_overlap(text, wiki_facts)
        confidence = round(1.0 - score, 3)
        label = 'fake' if confidence > 0.5 else 'real'

        return {
            'label': label,
            'confidence': confidence,
            'overlap_score': round(score, 3),
            'search_terms': search_terms
        }