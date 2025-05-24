class QueryGenerator:
    def __init__(self, min_entity_len=3, fallback_keywords=None, domain_filter=None):
        self.min_entity_len = min_entity_len
        self.fallback_keywords = fallback_keywords or []
        self.domain_filter = domain_filter

    def generate(self, entities):
        unique_entities = list({e.strip() for e in entities if len(e.strip()) >= self.min_entity_len})

        if not unique_entities and self.fallback_keywords:
            unique_entities = self.fallback_keywords

        quoted = [f'"{e}"' for e in unique_entities]

        # Base queries
        google_query = ' AND '.join(quoted)
        bing_query = ' OR '.join(quoted)
        duck_query = f'({" OR ".join(quoted)})'

        if self.domain_filter:
            google_query += f" {self.domain_filter}"
            bing_query += f" {self.domain_filter}"
            duck_query += f" {self.domain_filter}"

        return {
            "google": google_query,
            "bing": bing_query,
            "duckduckgo": duck_query
        }
