import os
import requests
import time

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    raise RuntimeError("Please set the BRAVE_API_KEY environment variable")

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "X-Subscription-Token": BRAVE_API_KEY
}

ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

def get_search_results(query, num_results=5):
    try:
        print("[LOG] --- [search.py] - Brave search")
        time.sleep(1.5)

        params = {
            "q": query,
            "count": num_results
        }
        resp = requests.get(ENDPOINT, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("web", {}).get("results", [])
        mapped = [
            {
                "title": r.get("title", ""),
                "href":  r.get("url", ""),
                "body":  r.get("description", "")
            }
            for r in items
        ]

        return [r["body"] for r in mapped]
    except Exception as e:
        print(f"[LOG] --- [search.py] - Search failed: {e}")
        return []

def get_search_results_complete(query, num_results=5):
    params = {
        "q": query,
        "count": num_results
    }
    resp = requests.get(ENDPOINT, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("web", {}).get("results", [])
    return [
        {
            "title": r.get("title", ""),
            "href":  r.get("url", ""),
            "body":  r.get("description", "")
        }
        for r in items
    ]
