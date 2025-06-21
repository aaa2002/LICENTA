from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class QueryGenerator:
    def __init__(self, model_path="src/agents/queryGen/querygen_model", min_entity_len=3, fallback_keywords=None, domain_filter=None,
                 max_length=128):
        self.min_entity_len = min_entity_len
        self.fallback_keywords = fallback_keywords or []
        self.domain_filter = domain_filter
        self.max_length = max_length

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    def generate(self, entities):
        unique_entities = list({e.strip() for e in entities if len(e.strip()) >= self.min_entity_len})

        if not unique_entities and self.fallback_keywords:
            unique_entities = self.fallback_keywords

        if not unique_entities:
            return {"google": "", "bing": "", "duckduckgo": ""}

        # Format input the same way as training
        entity_text = ", ".join(unique_entities)
        domain_text = f" [DOMAIN: {self.domain_filter}]" if self.domain_filter else ""
        input_text = f"Entities: {entity_text}{domain_text}"

        # Tokenize and generate
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, padding=True,
                                max_length=self.max_length)
        outputs = self.model.generate(**inputs, max_length=self.max_length)
        decoded_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "google": decoded_query,
            "bing": decoded_query,
            "duckduckgo": decoded_query  # or run through different models if needed
        }
