import joblib
import numpy as np


class FakeNewsAgent:
    def __init__(self,
                 vectorizer_path="model/tfidf_vectorizer.joblib",
                 model_path="model/fake_news_model.joblib",
                 encoder_path="model/label_encoder.joblib"):

        try:
            self.vectorizer = joblib.load(vectorizer_path)
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(encoder_path)

            # Verify we have exactly 2 classes
            if len(self.label_encoder.classes_) != 2:
                raise ValueError("Model should have exactly 2 classes (fake/real)")

        except Exception as e:
            raise RuntimeError(f"Failed to load model components: {str(e)}")

    def analyze(self, text):
        """Analyze text and return prediction with confidence"""
        try:
            X = self.vectorizer.transform([text])
            proba = self.model.predict_proba(X)[0]

            # Get prediction
            label_index = proba.argmax()
            label = self.label_encoder.inverse_transform([label_index])[0]
            confidence = round(proba[label_index], 3)

            return {
                "label": label,
                "confidence": confidence,
                "prob_fake": float(proba[0]),
                "prob_real": float(proba[1])
            }

        except Exception as e:
            return {
                "error": str(e),
                "label": "error",
                "confidence": 0.0
            }

    def update(self, text, true_label):
        """Update model with new labeled example"""
        try:
            # Convert numeric labels if needed
            if str(true_label) in ['0', '1']:
                true_label = 'fake' if str(true_label) == '0' else 'real'

            X = self.vectorizer.transform([text])
            y = self.label_encoder.transform([true_label])
            self.model.partial_fit(X, y, classes=[0, 1])
            return True
        except Exception as e:
            print(f"Update failed: {str(e)}")
            return False