import json

import joblib
import numpy as np
from delta import DeltaTable
from sklearn.feature_extraction.text import HashingVectorizer
from src.scraper.search import get_search_results
from src.scraper.llm import claim_to_question
from pyspark.sql import SparkSession
from src.agents.get_web.get_web import get_top_k_results_delta  # Your new unified logic

class StreamingFakeNewsAgent:
    def __init__(self,
                 vectorizer_path="src/agents/classic/saved_models/hashing_vectorizer.joblib",
                 model_path="src/agents/classic/saved_models/online_fake_news_model.joblib",
                 encoder_path="src/agents/classic/saved_models/label_encoder.joblib"):

        try:
            self.vectorizer = joblib.load(vectorizer_path)
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(encoder_path)

            if not isinstance(self.vectorizer, HashingVectorizer):
                raise ValueError("Vectorizer must be HashingVectorizer for streaming")
            if not hasattr(self.model, 'partial_fit'):
                raise ValueError("Model must support partial_fit for streaming")

        except Exception as e:
            raise RuntimeError(f"Initialization failed: {str(e)}")

    def analyze(self, text, web_text=None):

        if web_text:
            success = self.update(web_text, 'real')
            if not success:
                print(f"[LOG] --- [classic_agent.py] - Failed to update with web text: {web_text[:100]}...")

        try:
            X = self.vectorizer.transform([text])
            proba = self.model.predict_proba(X)[0]

            label_idx = np.argmax(proba)
            label = self.label_encoder.inverse_transform([label_idx])[0]

            return {
                'label': label,
                'confidence': float(proba[label_idx]),
                'probabilities': {
                    'fake': float(proba[0]),
                    'real': float(proba[1])
                }
            }
        except Exception as e:
            return {
                'error': str(e),
                'label': 'error',
                'confidence': 0.0
            }

    def update(self, text, true_label):
        try:
            if str(true_label) in ['0', '1']:
                true_label = 'fake' if str(true_label) == '0' else 'real'

            X = self.vectorizer.transform([text])
            y = self.label_encoder.transform([true_label])

            class_labels = list(self.label_encoder.transform(self.label_encoder.classes_))
            class_labels = sorted(set(class_labels))  # Ensure no weird order

            self.model.partial_fit(X, y, classes=class_labels)

            joblib.dump(self.model, "src/agents/classic/saved_models/online_fake_news_model.joblib")

            return True

        except Exception as e:
            print(f"[LOG] --- [classic_agent.py] - Update error: {str(e)}")
            print(f"[LOG] --- [classic_agent.py] - True label (raw): {true_label}")
            print(f"[LOG] --- [classic_agent.py] - Transformed y: {y}")
            print(f"[LOG] --- [classic_agent.py] - Classes used: {class_labels}")
            return False

    def batch_update(self, texts, labels):
        try:
            labels = [('fake' if str(l) in ['0', 'fake'] else 'real') for l in labels]

            X = self.vectorizer.transform(texts)
            y = self.label_encoder.transform(labels)

            self.model.partial_fit(X, y, classes=[0, 1])

            joblib.dump(self.model, "./saved_models/online_fake_news_model.joblib")

            return True
        except Exception as e:
            print(f"[LOG] --- [classic_agent.py] - Batch update error: {str(e)}")
            return False

    def analyze_with_scraper_update(self, text):
        try:
            question = claim_to_question(text)
            print(f"[LOG] --- [classic_agent.py] - Generated Question: {question}")

            search_results, web_text = get_top_k_results_delta(question, k=5)

            for result in search_results:
                success = self.update(result, 'real')
                if not success:
                    print(f"[LOG] --- [classic_agent.py] - Failed to update with result: {str(result)[:100]}...")

            result = self.analyze(text)
            return result

        except Exception as e:
            return {
                'error': str(e),
                'label': 'error',
                'confidence': 0.0
            }
