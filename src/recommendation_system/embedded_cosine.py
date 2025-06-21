from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from urllib.parse import urlparse
import pandas as pd

def load_iffy_sources(csv_path):
    df = pd.read_csv(csv_path)
    # Normalize domain names (strip spaces, lowercase)
    df['Domain'] = df['Domain'].str.strip().str.lower()
    iffy_dict = dict(zip(df['Domain'], df['Score']))
    return iffy_dict

IFFY_SOURCE_DICT = load_iffy_sources('src/recommendation_system/data/iffy-news.csv')

def assign_source_score(article):
    """
    Assigns a reputation score to an article based on its domain.
    Can be customized or extended with a lookup table or LLM later.
    """
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

    # Heuristic scoring
    for key, score in reputable_domains.items():
        if key in domain:
            return score

    for key, score in sketchy_domains.items():
        if key in domain:
            return score

    return default_score


def get_top_5_similar_articles(user_input, articles, top_k=5, alpha=0.6):
    """
    Recommends top_k articles based on semantic similarity + source credibility.
    alpha is the weight given to semantic similarity (vs source_score).
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    user_vector = model.encode(user_input)
    article_vectors = [model.encode(article['body']) for article in articles]

    similarities = cosine_similarity([user_vector], article_vectors)[0]

    combined_scores = []
    for i, article in enumerate(articles):
        source_score = article.get('source_score', assign_source_score(article))
        combined = alpha * similarities[i] + (1 - alpha) * source_score
        combined_scores.append(combined)
        articles[i]['source_score'] = source_score

    top_indices = heapq.nlargest(top_k, range(len(combined_scores)), key=lambda i: combined_scores[i])

    top_articles = [
        {
            'title': articles[i]['title'],
            'href': articles[i]['href'],
            'body': articles[i]['body'],
            'similarity': float(similarities[i]),
            'source_score': float(articles[i]['source_score']),
            'combined_score': float(combined_scores[i])
        }
        for i in top_indices
    ]

    return top_articles
