"""Treina e compara modelos de ML para classificar a area do curriculo.
Dataset: Kaggle 'Resume Dataset' (snehaanbhawal/resume-dataset) -> data/Resume.csv
Colunas: Resume_str, Category (ou Resume, Category)."""
import pandas as pd, joblib, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from preprocess import limpar_texto

df = pd.read_csv("data/Resume.csv")
col = "Resume_str" if "Resume_str" in df.columns else "Resume"
df = df[[col, "Category"]].dropna().drop_duplicates()          # limpeza (Aula 02)
df["texto"] = df[col].map(limpar_texto)
print(df["Category"].value_counts())

Xtr, Xte, ytr, yte = train_test_split(df["texto"], df["Category"], test_size=0.2,
                                      stratify=df["Category"], random_state=42)
tfidf = lambda: TfidfVectorizer(max_features=8000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
modelos = {
    "LogisticRegression": LogisticRegression(max_iter=2000, C=10),
    "RandomForest": RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1),
    "MLP (Perceptron multicamada)": MLPClassifier(hidden_layer_sizes=(256, 64), early_stopping=True, max_iter=200, random_state=42),
}
res, melhor, melhor_f1 = [], None, -1
for nome, clf in modelos.items():
    pipe = Pipeline([("tfidf", tfidf()), ("clf", clf)]).fit(Xtr, ytr)
    pred = pipe.predict(Xte)
    acc, f1 = accuracy_score(yte, pred), f1_score(yte, pred, average="macro")
    res.append({"modelo": nome, "acuracia": round(acc, 4), "f1_macro": round(f1, 4)})
    print(nome, acc, f1)
    if f1 > melhor_f1: melhor, melhor_f1, melhor_nome, melhor_pred = pipe, f1, nome, pred

pd.DataFrame(res).to_csv("models/comparacao_modelos.csv", index=False)
print("\nMELHOR:", melhor_nome); print(classification_report(yte, melhor_pred))
labels = sorted(df["Category"].unique())
plt.figure(figsize=(12, 10))
sns.heatmap(confusion_matrix(yte, melhor_pred, labels=labels), xticklabels=labels, yticklabels=labels, cmap="Blues")
plt.title(f"Matriz de confusao - {melhor_nome}"); plt.tight_layout(); plt.savefig("models/matriz_confusao.png", dpi=150)
joblib.dump(melhor, "models/classificador.joblib")
