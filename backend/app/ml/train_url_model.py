import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datasets import load_dataset
import sys

# Ensure backend path is in sys.path so we can import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from backend.app.services.normalizer import normalize_url
from backend.app.services.extractor import StaticFeatureExtractor

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'models')

def load_data():
    print("Loading 'alexkstern/phishing_urls' dataset from Hugging Face...")
    ds1 = load_dataset("alexkstern/phishing_urls")
    df1 = ds1['train'].to_pandas() if 'train' in ds1 else ds1[list(ds1.keys())[0]].to_pandas()
    
    if 'text' in df1.columns and 'url' not in df1.columns:
        df1.rename(columns={'text': 'url'}, inplace=True)
    elif 'URL' in df1.columns and 'url' not in df1.columns:
        df1.rename(columns={'URL': 'url'}, inplace=True)
        
    print("Loading 'Mitake/PhishingURLsANDBenignURLs' dataset from Hugging Face...")
    ds2 = load_dataset("Mitake/PhishingURLsANDBenignURLs")
    df2 = ds2['train'].to_pandas() if 'train' in ds2 else ds2[list(ds2.keys())[0]].to_pandas()
    
    df = pd.concat([df1, df2], ignore_index=True)
    df.drop_duplicates(subset=['url'], inplace=True)
    df.dropna(subset=['url', 'label'], inplace=True)
    
    if len(df) > 50000:
        df, _ = train_test_split(df, train_size=50000, stratify=df['label'], random_state=42)
    
    return df

def extract_structural(df):
    print("Extracting structural features (this may take a minute)...")
    extractor = StaticFeatureExtractor()
    feature_keys = [
        "url_length", "hostname_length", "path_length", "num_subdomains", 
        "num_dots", "num_hyphens", "num_special_chars", "is_ip_address",
        "hostname_entropy", "path_entropy"
    ]
    
    X_struct = []
    for url in df['url']:
        norm = normalize_url(str(url))
        if "Failed to parse URL" in norm.get("normalization_changes", []):
            X_struct.append([0.0] * len(feature_keys))
            continue
        feats = extractor.extract(norm)
        row = [float(feats.get(k, 0)) for k in feature_keys]
        X_struct.append(row)
        
    return np.array(X_struct)

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_data()
    
    X_raw = df['url'].astype(str).to_numpy()
    y = df['label'].astype(int).to_numpy()
    X_struct = extract_structural(df)
    
    print("Splitting dataset (80/20)...")
    # Split indices so we keep lexical and structural aligned
    indices = np.arange(len(y))
    idx_train, idx_test, y_train, y_test = train_test_split(indices, y, test_size=0.20, random_state=42, stratify=y)
    
    X_raw_train = X_raw[idx_train]
    X_raw_test = X_raw[idx_test]
    
    X_struct_train = X_struct[idx_train]
    X_struct_test = X_struct[idx_test]
    
    # 1. Train Lexical Model
    print("Training Lexical Pipeline (TF-IDF + LR)...")
    lex_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=20000)),
        ('clf', LogisticRegression(max_iter=1000, C=10, random_state=42, n_jobs=-1))
    ])
    lex_pipeline.fit(X_raw_train, y_train)
    y_pred_lex = lex_pipeline.predict(X_raw_test)
    
    # 2. Train Structural Model
    print("Training Structural Pipeline (HistGradientBoosting)...")
    struct_clf = HistGradientBoostingClassifier(random_state=42)
    struct_clf.fit(X_struct_train, y_train)
    y_pred_struct = struct_clf.predict(X_struct_test)
    
    # Evaluate Lexical
    acc_lex = accuracy_score(y_test, y_pred_lex)
    prec_lex = precision_score(y_test, y_pred_lex)
    rec_lex = recall_score(y_test, y_pred_lex)
    f1_lex = f1_score(y_test, y_pred_lex)
    print(f"Lexical -> Acc: {acc_lex:.4f} | Prec: {prec_lex:.4f} | Rec: {rec_lex:.4f} | F1: {f1_lex:.4f}")
    
    # Evaluate Structural
    acc_struct = accuracy_score(y_test, y_pred_struct)
    prec_struct = precision_score(y_test, y_pred_struct)
    rec_struct = recall_score(y_test, y_pred_struct)
    f1_struct = f1_score(y_test, y_pred_struct)
    print(f"Structural -> Acc: {acc_struct:.4f} | Prec: {prec_struct:.4f} | Rec: {rec_struct:.4f} | F1: {f1_struct:.4f}")
    
    print("\nSaving models...")
    joblib.dump(lex_pipeline, os.path.join(MODEL_DIR, 'phishing_lexical_model.pkl'))
    joblib.dump(struct_clf, os.path.join(MODEL_DIR, 'phishing_structural_model.pkl'))
    
    metadata = {
        "models": {
            "lexical": {
                "type": "TFIDF_Char_LogisticRegression",
                "accuracy": acc_lex,
                "precision": prec_lex,
                "recall": rec_lex,
                "f1": f1_lex
            },
            "structural": {
                "type": "HistGradientBoostingClassifier",
                "features": [
                    "url_length", "hostname_length", "path_length", "num_subdomains", 
                    "num_dots", "num_hyphens", "num_special_chars", "is_ip_address",
                    "hostname_entropy", "path_entropy"
                ],
                "accuracy": acc_struct,
                "precision": prec_struct,
                "recall": rec_struct,
                "f1": f1_struct
            }
        },
        "training_samples": len(y_train)
    }
    
    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main()
