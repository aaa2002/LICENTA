from duckduckgo_search import DDGS

# === Step 2: DuckDuckGo Search ===
def get_search_results(query, num_results=5):
    with DDGS() as ddgs:
        return [r["body"] for r in ddgs.text(query, max_results=num_results)]