from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from urllib.parse import urlparse
import pandas as pd
import numpy as np

def load_iffy_sources(csv_path):
    df = pd.read_csv(csv_path)
    df['Domain'] = df['Domain'].str.strip().str.lower()
    iffy_dict = dict(zip(df['Domain'], df['Score']))
    return iffy_dict

IFFY_SOURCE_DICT = load_iffy_sources('src/recommendation_system/data/iffy-news.csv')

def assign_source_score(article):
    domain = urlparse(article['href']).netloc.lower()

    reputable_domains = {
        'wikipedia.org': 0.95,
        'bbc.com': 0.9,
        'nytimes.com': 0.9,
        'reuters.com': 0.9,
        'nasa.gov': 0.95,
        'nature.com': 0.95,
        'scientificamerican.com': 0.9
    }

    sketchy_domains = {
        'youtube.com': 0.2,
        'beforeitsnews.com': 0.1,
        'theonion.com': 0.05,
        'infowars.com': 0.05
    }

    default_score = 0.5

    for key in IFFY_SOURCE_DICT:
        if key in domain:
            return float(IFFY_SOURCE_DICT[key])

    for key, score in reputable_domains.items():
        if key in domain:
            return score

    for key, score in sketchy_domains.items():
        if key in domain:
            return score

    return default_score


def get_top_5_similar_articles(user_input, articles, top_k=5, alpha=0.6):

    if not articles:
        return []

    model = SentenceTransformer('all-MiniLM-L6-v2')
    user_vector = model.encode(user_input)

    filtered_articles = [article for article in articles if article.get('body')]
    if not filtered_articles:
        return []

    article_vectors = [model.encode(article['body']) for article in filtered_articles]

    article_vectors = np.array(article_vectors)
    if article_vectors.ndim != 2:
        raise ValueError("article_vectors must be a 2D array")

    similarities = cosine_similarity([user_vector], article_vectors)[0]

    combined_scores = []
    for i, article in enumerate(filtered_articles):
        source_score = article.get('source_score', assign_source_score(article))
        combined = alpha * similarities[i] + (1 - alpha) * source_score
        combined_scores.append(combined)
        article['source_score'] = source_score

    top_indices = heapq.nlargest(min(top_k, len(combined_scores)), range(len(combined_scores)),
                                 key=lambda i: combined_scores[i])

    top_articles = [
        {
            'title': filtered_articles[i]['title'],
            'href': filtered_articles[i]['href'],
            'body': filtered_articles[i]['body'],
            'similarity': float(similarities[i]),
            'source_score': float(filtered_articles[i]['source_score']),
            'combined_score': float(combined_scores[i])
        }
        for i in top_indices
    ]

    return top_articles
