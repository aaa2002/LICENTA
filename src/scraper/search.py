from duckduckgo_search import DDGS

def get_search_results(query, num_results=5):
    with DDGS() as ddgs:
        print("[LOG] --- [search.py] - DuckDuckGo search")
        return [r["body"] for r in ddgs.text(query, max_results=num_results)]

def get_search_results_complete (query, num_results=5):
    with DDGS() as ddgs:
        return [r for r in ddgs.text(query, max_results=num_results)]
