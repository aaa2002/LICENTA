from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_re_model():
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    return tokenizer, model