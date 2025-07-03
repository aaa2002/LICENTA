from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import pandas as pd
import numpy as np

df_fake = pd.read_csv("../../filtered/filtered_fake.csv")
df_real = pd.read_csv("../../filtered/filtered_real.csv")
df = pd.concat([df_fake, df_real], ignore_index=True)

df = df.dropna(subset=["text"])
df = df[df["text"].str.strip().astype(bool)]

df['truth'] = df['truth'].map({0: 'fake', 1: 'real', '0': 'fake', '1': 'real'}).fillna(df['truth'])

print("Label distribution:")
print(df['truth'].value_counts(normalize=True))

vectorizer = HashingVectorizer(
    n_features=2**20,
    alternate_sign=False,
    stop_words='english'
)

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['truth'])

X = vectorizer.transform(df['text'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = SGDClassifier(
    loss='log_loss',
    penalty='l2',
    max_iter=1000,
    tol=1e-3,
    early_stopping=False,
    random_state=42
)

classes = np.unique(y_train)
print("\nTraining model (partial_fit)...")
model.partial_fit(X_train, y_train, classes=classes)

print("\nFinal Evaluation:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

joblib.dump(vectorizer, "./saved_models/hashing_vectorizer.joblib")
joblib.dump(model, "./saved_models/online_fake_news_model.joblib")
joblib.dump(label_encoder, "./saved_models/label_encoder.joblib")

print("\nModel saved successfully! Ready for streaming updates.")
