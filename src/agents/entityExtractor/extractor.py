import spacy

class Extractor:
    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    def extract(self, text):
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in {
            "PERSON", "ORG", "GPE", "PRODUCT", "EVENT", "WORK_OF_ART", "LOC"
        }]
