from langchain_core.runnables import Runnable
import csv
import os

def label_to_bool(label):
    return 1 if label.lower() == 'real' else 0

def float_to_label(value, threshold=0.75):
    return 'real' if value >= threshold else 'fake'

class Aggregator(Runnable):
    def invoke(self, input: dict, config=None) -> dict:
        fn = input["fn_result"]
        wiki = input["wiki_result"]
        scraper = input["scraper_result"]
        coherence = input["coherence_result"]

        # Apply weights
        weighted_score = (
            label_to_bool(fn["label"]) * fn["confidence"] * 0.19 +
            label_to_bool(wiki["label"]) * wiki["confidence"] * 0.23 +
            label_to_bool(coherence["label"]) * coherence["confidence"] * 0.17 +
            label_to_bool(scraper["label"]) * scraper["confidence"] * 0.41
        )

        final_label = float_to_label(weighted_score, threshold=0.41)
        score = round(weighted_score, 4)

        csv_data = {
            "fn_label": fn["label"],
            "fn_confidence": fn["confidence"],
            "wiki_label": wiki["label"],
            "wiki_confidence": wiki["confidence"],
            "scraper_label": scraper["label"],
            "scraper_confidence": scraper["confidence"],
            "coherence_label": coherence["label"],
            "coherence_confidence": coherence["confidence"],
            "final_score": score,
            "final_label": final_label
        }

        file_path = "aggregator_output.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=csv_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(csv_data)

        return {
            "final_label": final_label,
            "score": score,
            "details": input
        }
