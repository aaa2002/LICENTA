import requests
from bs4 import BeautifulSoup
import json
import os
from transformers import pipeline
from newspaper import Article


def duckduckgo_news_search(query, num_results=10):
    """Search DuckDuckGo for news articles and return top links."""
    search_url = f"https://lite.duckduckgo.com/lite/?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for result in soup.select("a.result-link")[:num_results]:  # DuckDuckGo Lite results
        title = result.text
        link = result["href"]
        articles.append((title, link))

    return articles


def fetch_and_clean_text(url):
    """Fetch and extract readable text from a webpage."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
        return None


def save_results(results):
    # Check if the output folder exists and create it if it doesn't
    if not os.path.exists("./output"):
        os.makedirs("./output")

    # Check if the file already exists and delete it if it does
    if os.path.exists("./output/scraped_results.json"):
        os.remove("./output/scraped_results.json")

    with open("./output/scraped_results.json", "w") as f:
        json.dump(results, f, indent=4)


def classify_articles(articles):
    """Classify scraped articles as true or false."""
    fact_check_pipeline = pipeline("zero-shot-classification", model="distilbert-base-uncased")
    labels = ["true", "false", "uncertain"]

    for title, url in articles:
        text = fetch_and_clean_text(url)
        if text:
            result = fact_check_pipeline(text, candidate_labels=labels)
            prediction = result["labels"][0]
            confidence = round(result["scores"][0] * 100, 2)
            print(f"\n📰 Article: {title}")
            print(f"🤖 AI: Prediction: {prediction} (Confidence: {confidence}%)")


if __name__ == "__main__":
    query = input("Enter a keyword or phrase to search on DuckDuckGo News: ")
    print(f"\n🔍 Searching for: {query}\n")

    articles = duckduckgo_news_search(query)
    results = [{"title": title, "url": url} for title, url in articles]

    for i, (title, url) in enumerate(articles, start=1):
        print(f"{i}. {title}")
        print(f"   🔗 URL: {url}\n")

    save_results(results)
    classify_articles(articles)
