import spacy_transformers
import spacy

nlp = spacy.load("en_core_web_trf")
doc = nlp("Trump is president of the United States.")

for ent in doc.ents:
    print(ent.text, ent.label_)

