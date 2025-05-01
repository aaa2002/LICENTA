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
from take2.agents.classic.classic_agent import StreamingFakeNewsAgent
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
import time
from tqdm import tqdm  # For progress bar (install with pip install tqdm)
from take2.scraper.search import get_search_results
from take2.scraper.llm import claim_to_question

def run_tests(input_csv, output_csv):
    # Load data
    print(f"\nLoading test data from {input_csv}...")
    df = pd.read_csv(input_csv)

    # Convert numeric labels if present
    if set(df['label'].unique()).issubset({0, 1, '0', '1'}):
        df['true_label'] = df['label'].map({'0': 'fake', 0: 'fake', '1': 'real', 1: 'real'})
    else:
        df['true_label'] = df['label']

    # Initialize agent with timing
    print("Initializing FakeNewsAgent...")
    start_time = time.time()
    agent = StreamingFakeNewsAgent()
    init_time = time.time() - start_time
    print(f"Agent initialized in {init_time:.2f} seconds")

    # Process each text with progress bar
    results = []
    print("\nRunning predictions...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:

            # querying ollama nad duckduckgo to update model
            claim = row['text']
            question = claim_to_question(claim)
            search_results = get_search_results(question)
            # Update agent with new data
            print(f"Claim: {claim}\n"
                  f"Question: {question}\n"
                  f"Search Results: {search_results}\n")
            for result in search_results:
                agent.update(result, 'real')

            result = agent.analyze(row['text'])

            results.append({
                'text_id': row.get('id', _),  # Keep original ID if exists
                'text': row['text'][:100] + '...' if len(row['text']) > 100 else row['text'],
                'true_label': row['true_label'],
                'predicted_label': result.get('label', 'error'),
                'confidence': result.get('confidence', 0),
                'prob_fake': result.get('prob_fake', 0),
                'prob_real': result.get('prob_real', 0),
                'error': result.get('error', None)
            })
        except Exception as e:
            results.append({
                'text_id': row.get('id', _),
                'text': row['text'][:100] + '...' if len(row['text']) > 100 else row['text'],
                'true_label': row['true_label'],
                'predicted_label': 'error',
                'confidence': 0,
                'error': str(e)
            })

    # Create results dataframe
    results_df = pd.DataFrame(results)

    # Calculate correctness (skip errored predictions)
    results_df['correct'] = results_df.apply(
        lambda x: str(x['true_label']).lower() == str(x['predicted_label']).lower()
        if x['error'] is None else None,
        axis=1
    )

    # Save results with timestamp
    results_df.to_csv(output_csv, index=False)
    print(f"\nResults saved to {output_csv}")

    # Calculate and print metrics
    valid_predictions = results_df[results_df['error'].isna()]

    if len(valid_predictions) > 0:
        # Basic metrics
        accuracy = valid_predictions['correct'].mean()
        error_rate = 1 - (len(valid_predictions) / len(results_df))

        # Precision, recall, F1
        y_true = valid_predictions['true_label'].str.lower()
        y_pred = valid_predictions['predicted_label'].str.lower()

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='weighted', zero_division=0
        )

        print("\n=== Evaluation Metrics ===")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Error Rate: {error_rate:.2%}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")

        # Confidence analysis
        print("\n=== Confidence Analysis ===")
        print("Average confidence for correct predictions: "
              f"{valid_predictions[valid_predictions['correct']]['confidence'].mean():.2f}")
        print("Average confidence for incorrect predictions: "
              f"{valid_predictions[~valid_predictions['correct']]['confidence'].mean():.2f}")

        # Confusion matrix
        print("\n=== Confusion Matrix ===")
        print(pd.crosstab(
            valid_predictions['true_label'].str.lower(),
            valid_predictions['predicted_label'].str.lower(),
            rownames=['True'],
            colnames=['Predicted'],
            margins=True
        ))
    else:
        print("\nNo valid predictions to evaluate!")

    # Print error summary if any
    if len(results_df[~results_df['error'].isna()]) > 0:
        print("\n=== Prediction Errors ===")
        print(f"Total errors: {len(results_df[~results_df['error'].isna()])}")
        print("Error samples:")
        print(results_df[~results_df['error'].isna()][['text_id', 'error']].head())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default="data/test_set_100.csv", help="Input CSV file")
    parser.add_argument('--output', default="data/test_results.csv", help="Output CSV file")
    args = parser.parse_args()

    run_tests(
        input_csv=args.input,
        output_csv=args.output
    )