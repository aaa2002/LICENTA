from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# === Step 3: Load REBEL for Relation Extraction ===
def load_re_model():
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    return tokenizer, model