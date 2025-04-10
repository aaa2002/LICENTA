from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd

df_fake = pd.read_csv("../filtered/filtered_fake.csv")
df_real = pd.read_csv("../filtered/filtered_real.csv")

df = pd.concat([df_fake, df_real], ignore_index=True)

df = df.dropna(subset=["text"])
df = df[df["text"].str.strip().astype(bool)]

X = df["text"]
y = df["truth"]

tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_tfidf = tfidf.fit_transform(X)
model = LogisticRegression()
model.fit(X_tfidf, y)

joblib.dump(tfidf, "../model/tfidf_vectorizer.joblib")
joblib.dump(model, "../model/fake_news_model.joblib")

print("Model and vectorizer saved to /model")
