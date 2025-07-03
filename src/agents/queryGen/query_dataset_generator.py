import json
import joblib
import re
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = joblib.load("src/agents/queryGen/querygen_model.joblib")
model.to(device).eval()

tokenizer = T5Tokenizer.from_pretrained("src/agents/queryGen/querygen_model")

RE_GOOGLE    = re.compile(r'"google"\s*:\s*"([^"]*)"', re.IGNORECASE)
RE_BING      = re.compile(r'"bing"\s*:\s*"([^"]*)"', re.IGNORECASE)
RE_DUCKDUCKGO= re.compile(r'"duckduckgo"\s*:\s*"([^"]*)"', re.IGNORECASE)

def generate_query(headline: str) -> dict:
    input_str = "generate queries: " + headline
    toks = tokenizer(input_str, return_tensors="pt", truncation=True, padding=True)
    input_ids = toks.input_ids.to(device)
    attention_mask = toks.attention_mask.to(device)

    out_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=64,
        num_beams=4,
        early_stopping=True
    )

    raw = tokenizer.decode(out_ids[0].cpu(), skip_special_tokens=False)
    print("raw decoded:", repr(raw))

    cleaned = raw.replace("<pad>", "").strip()
    cleaned = cleaned.replace("<unk>", '"')
    print("cleaned decoded:", repr(cleaned))

    def extract(regex):
        m = regex.search(cleaned)
        return m.group(1) if m else ""

    google_q    = extract(RE_GOOGLE)
    bing_q      = extract(RE_BING)
    duckduckgo_q= extract(RE_DUCKDUCKGO)

    return {
        "google": google_q,
        "bing":   bing_q,
        "duckduckgo": duckduckgo_q
    }
