import pandas as pd
import joblib
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent.parent / "training data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
DEFAULT_DATA_PATH = BASE_DIR / "data" / "sms_spam_dataset.csv"


def _load_sms_spam_csv(path, label_col, text_col, sep=","):
    df = pd.read_csv(path, encoding="latin1", sep=sep)
    unnamed = [c for c in df.columns if "Unnamed" in c]
    if unnamed:
        df = df.drop(columns=unnamed)
    df = df[[label_col, text_col]].copy()
    df.columns = ["label", "text"]
    df["label"] = df["label"].map(lambda x: 1 if str(x).strip().lower() == "spam" else 0)
    return df


def _load_email_dataset(path, label_value=1):
    df = pd.read_csv(path, encoding="latin1")
    body_col = "body" if "body" in df.columns else "text_combined"
    if "subject" in df.columns and body_col in df.columns:
        df["text"] = df["subject"].fillna("") + " " + df[body_col].fillna("")
    elif body_col in df.columns:
        df["text"] = df[body_col].fillna("")
    else:
        df["text"] = df.iloc[:, 0].fillna("")
    df["label"] = label_value
    return df[["label", "text"]]


def _load_phishing_legit(path):
    df = pd.read_csv(path, encoding="latin1")
    if "text" in df.columns and "label" in df.columns:
        return df[["label", "text"]].copy()
    if "subject" in df.columns and "body" in df.columns and "label" in df.columns:
        df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")
        return df[["label", "text"]].copy()
    return None


def _load_email_with_label(path):
    df = pd.read_csv(path, encoding="latin1")
    body_col = "body" if "body" in df.columns else "text_combined"
    if "subject" in df.columns and body_col in df.columns:
        df["text"] = df["subject"].fillna("") + " " + df[body_col].fillna("")
    else:
        df["text"] = df[body_col].fillna("")
    return df[["label", "text"]].copy()


def load_all_data():
    datasets = []

    # 1. SMS Spam Collection (already in repo)
    try:
        df = pd.read_csv(DEFAULT_DATA_PATH, names=["label", "text"])
        df["label"] = df["label"].map(lambda x: 1 if str(x).strip().lower() == "spam" else 0)
        datasets.append(df)
        print(f"[Load] sms_spam_dataset.csv: {len(df)} rows")
    except Exception as e:
        print(f"[Load] sms_spam_dataset.csv skipped: {e}")

    # 1.5. Tricky Test Scenarios
    try:
        tricky_path = BASE_DIR / "data" / "tricky_test_scenarios.json"
        if tricky_path.exists():
            tricky_df = pd.read_json(tricky_path)
            tricky_df = tricky_df.rename(columns={"is_scam": "label"})
            tricky_df = tricky_df[["label", "text"]].copy()
            datasets.append(tricky_df)
            print(f"[Load] tricky_test_scenarios.json: {len(tricky_df)} rows")
    except Exception as e:
        print(f"[Load] tricky_test_scenarios.json skipped: {e}")


    training_dir = DATA_DIR if DATA_DIR.exists() else None

    if training_dir:
        # 2. spam_sms.csv
        spam_sms = training_dir / "spam_sms.csv"
        if spam_sms.exists():
            df = _load_sms_spam_csv(spam_sms, "v1", "v2")
            datasets.append(df)
            print(f"[Load] spam_sms.csv: {len(df)} rows")

        # 3. spam.csv (same format, extra unnamed cols)
        spam = training_dir / "spam.csv"
        if spam.exists():
            df = _load_sms_spam_csv(spam, "v1", "v2")
            datasets.append(df)
            print(f"[Load] spam.csv: {len(df)} rows")

        # 4. scam.csv
        scam = training_dir / "scam.csv"
        if scam.exists():
            df = _load_sms_spam_csv(scam, "class", "message")
            datasets.append(df)
            print(f"[Load] scam.csv: {len(df)} rows")

        # 5. Nigerian_Fraud.csv (all are fraud = label 1)
        nf = training_dir / "Nigerian_Fraud.csv"
        if nf.exists():
            df = _load_email_dataset(nf, label_value=1)
            datasets.append(df)
            print(f"[Load] Nigerian_Fraud.csv: {len(df)} rows")

        # 6. phishing_email.csv (label column is 0/1)
        pe = training_dir / "phishing_email.csv"
        if pe.exists():
            df = _load_email_with_label(pe)
            datasets.append(df)
            print(f"[Load] phishing_email.csv: {len(df)} rows")

        # 7. phishing_legit_dataset_KD_10000.csv
        pl = training_dir / "phishing_legit_dataset_KD_10000.csv"
        if pl.exists():
            df = _load_phishing_legit(pl)
            if df is not None:
                datasets.append(df)
                print(f"[Load] phishing_legit_dataset_KD_10000.csv: {len(df)} rows")

        # 8. Enron.csv (all legitimate business = label 0)
        enron = training_dir / "Enron.csv"
        if enron.exists():
            df = _load_email_dataset(enron, label_value=0)
            datasets.append(df)
            print(f"[Load] Enron.csv: {len(df)} rows")

        # 9. CEAS_08.csv
        ceas = training_dir / "CEAS_08.csv"
        if ceas.exists():
            df = _load_email_with_label(ceas)
            datasets.append(df)
            print(f"[Load] CEAS_08.csv: {len(df)} rows")

        # 10. Ling.csv
        ling = training_dir / "Ling.csv"
        if ling.exists():
            df = _load_email_with_label(ling)
            datasets.append(df)
            print(f"[Load] Ling.csv: {len(df)} rows")

        # 11. Nazario.csv
        nazario = training_dir / "Nazario.csv"
        if nazario.exists():
            df = _load_email_with_label(nazario)
            datasets.append(df)
            print(f"[Load] Nazario.csv: {len(df)} rows")

        # 12. SpamAssasin.csv
        sa = training_dir / "SpamAssasin.csv"
        if sa.exists():
            df = _load_email_with_label(sa)
            datasets.append(df)
            print(f"[Load] SpamAssasin.csv: {len(df)} rows")

        # 13. Synthetic augmented data (covers modern scam patterns)
        syn = training_dir / "synthetic_augmented.csv"
        if syn.exists():
            df = pd.read_csv(syn)
            df["label"] = df["label"].astype(int)
            datasets.append(df)
            print(f"[Load] synthetic_augmented.csv: {len(df)} rows")

    combined = pd.concat(datasets, ignore_index=True)
    combined = combined.dropna(subset=["text"])
    combined["text"] = combined["text"].astype(str)
    combined = combined[combined["text"].str.strip() != ""]
    return combined


def train():
    print("[Train] Loading all datasets...")
    df = load_all_data()
    print(f"[Train] Combined dataset: {len(df)} samples ({df['label'].value_counts().to_dict()})")

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words="english",
        sublinear_tf=True,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(C=1.0, max_iter=1000, random_state=42, class_weight="balanced")
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"[Train] Accuracy: {acc:.4f}")
    print(f"[Train] F1 Score: {f1:.4f}")
    print(classification_report(y_test, y_pred, target_names=["legit", "fraud"]))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    vec_path = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
    clf_path = ARTIFACTS_DIR / "fraud_classifier.joblib"
    joblib.dump(vectorizer, vec_path)
    joblib.dump(clf, clf_path)
    print(f"[Train] Saved vectorizer -> {vec_path}")
    print(f"[Train] Saved classifier -> {clf_path}")
    print("[Train] Done.")


if __name__ == "__main__":
    train()
