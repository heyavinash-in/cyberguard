import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from datasets import load_dataset
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from backend.app.services.message_extractor import preprocess_text

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'models', 'message')

import glob

def load_data():
    print("Loading local kagglehub dataset...")
    DATASET_PATH = 'C:/Users/phoen/.cache/kagglehub/datasets/uciml/sms-spam-collection-dataset/versions/1/*.csv'
    files = glob.glob(DATASET_PATH)
    if not files:
        raise ValueError("Dataset not found at expected path")
        
    df = pd.read_csv(files[0], encoding='latin-1')
    if 'v1' in df.columns and 'v2' in df.columns:
        df = df.rename(columns={"v1": "label", "v2": "message"})
    
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    df.drop_duplicates(subset=['message'], inplace=True)
    df.dropna(subset=['message', 'label'], inplace=True)
    
    return df

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_data()
    
    print("Preprocessing messages (this includes normalization)...")
    df['clean_message'] = df['message'].apply(preprocess_text)
    
    X = df['clean_message'].to_numpy()
    y = df['label'].to_numpy()
    
    print("Splitting dataset (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    # 1. Word TF-IDF Pipeline
    print("Training Word TF-IDF Pipeline...")
    word_pipeline = Pipeline([
        ('tfidf_word', TfidfVectorizer(analyzer='word', ngram_range=(1, 2), sublinear_tf=True, min_df=2, max_features=10000)),
        ('clf_word', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
    ])
    
    # 2. Character TF-IDF Pipeline
    print("Training Character TF-IDF Pipeline...")
    char_pipeline = Pipeline([
        ('tfidf_char', TfidfVectorizer(analyzer='char', ngram_range=(3, 5), sublinear_tf=True, min_df=2, max_features=15000)),
        ('clf_char', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42))
    ])
    
    # 3. Ensemble
    print("Training Ensemble (Soft Voting)...")
    ensemble = VotingClassifier(
        estimators=[('word', word_pipeline), ('char', char_pipeline)],
        voting='soft'
    )
    
    ensemble.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating Ensemble...")
    y_pred = ensemble.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 (Phishing): {f1:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    
    print("\nSaving models...")
    joblib.dump(ensemble, os.path.join(MODEL_DIR, 'message_ensemble_model.pkl'))
    
    metadata = {
        "model_version": "message-v1",
        "models": {
            "ensemble": {
                "type": "VotingClassifier(Word+Char TF-IDF)",
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "macro_f1": macro_f1,
                "confusion_matrix": cm
            }
        },
        "training_samples": len(y_train),
        "validation_samples": len(y_test)
    }
    
    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print("Done! Artifacts saved.")

if __name__ == "__main__":
    main()
