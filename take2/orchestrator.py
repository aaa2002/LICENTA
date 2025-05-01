# from agents.classic import FakeNewsAgent
# from agents.wiki_check import WikiAgent
# from agents.coherence import CoherenceAgent
# from take2.agents.scrape.main import ScraperAgent
#
# if __name__ == "__main__":
#     text = "Breaking news: Aliens have landed in Times Square to discuss trade deals."
#
#     fake_news_agent = FakeNewsAgent()
#     fn_result = fake_news_agent.analyze(text)
#
#     wiki_agent = WikiAgent()
#     wiki_result = wiki_agent.analyze(text)
#
#     coherence_agent = CoherenceAgent()
#     coherence_result = coherence_agent.analyze(text)
#
#     scraper_agent = ScraperAgent()
#     scraper_result = scraper_agent.analyze(text)
#
#     print("\nFake News Analysis Result:")
#     print(fn_result)
#
#     print("\nWikipedia Knowledge Result:")
#     print(wiki_result)
#
#     print("\nText Coherence Analysis Result:")
#     print(coherence_result)
#
#     print("\nScraper Analysis Result:")
#     print(scraper_result)

import pandas as pd
from take2.agents.classic import FakeNewsAgent

def run_tests(input_csv, output_csv):
    # Load data
    df = pd.read_csv(input_csv)

    # Convert numeric labels if present
    if set(df['label'].unique()).issubset({0, 1, '0', '1'}):
        df['true_label'] = df['label'].map({'0': 'fake', 0: 'fake', '1': 'real', 1: 'real'})
    else:
        df['true_label'] = df['label']

    # Initialize agent
    agent = FakeNewsAgent()

    # Process each text
    results = []
    for _, row in df.iterrows():
        result = agent.analyze(row['text'])

        results.append({
            'text': row['text'][:100] + '...' if len(row['text']) > 100 else row['text'],
            'true_label': row['true_label'],
            'predicted_label': result.get('label', 'error'),
            'confidence': result.get('confidence', 0),
            'prob_fake': result.get('prob_fake', 0),
            'prob_real': result.get('prob_real', 0),
            'correct': str(row['true_label']).lower() == str(result.get('label', '')).lower()
        })

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)

    # Calculate metrics
    accuracy = results_df['correct'].mean()
    print(f"Accuracy: {accuracy:.2%}")

    # Confusion matrix
    print("\nConfusion Matrix:")
    print(pd.crosstab(
        results_df['true_label'].str.lower(),
        results_df['predicted_label'].str.lower(),
        rownames=['True'],
        colnames=['Predicted'],
        margins=True
    ))


if __name__ == "__main__":
    run_tests(
        input_csv="data/test_set_100.csv",
        output_csv="data/test_results.csv"
    )