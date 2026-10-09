import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datasets import load_dataset

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

def load_and_prepare_data():
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
    
    # Merge datasets
    df = pd.concat([df1, df2], ignore_index=True)
    
    print(f"Total raw rows: {len(df)}")
    
    df.drop_duplicates(subset=['url'], inplace=True)
    df.dropna(subset=['url', 'label'], inplace=True)
    print(f"Rows after deduplication: {len(df)}")
    
    # We can easily train on 200k rows with TF-IDF and Logistic Regression
    if len(df) > 200000:
        df, _ = train_test_split(df, train_size=200000, stratify=df['label'], random_state=42)
        print(f"Sampled down to {len(df)} rows to balance speed and accuracy.")
    
    return df

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_and_prepare_data()
    
    X = df['url'].astype(str).to_numpy()
    y = df['label'].astype(int).to_numpy()
    
    print("Splitting dataset (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Testing set: {len(X_test)} samples")
    
    print("Training TF-IDF + Logistic Regression Pipeline...")
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=50000)),
        ('clf', LogisticRegression(max_iter=2000, C=10, random_state=42, n_jobs=-1))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nPipeline -> Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")
    
    print("\nSaving best model and artifacts...")
    model_path = os.path.join(MODEL_DIR, 'phishing_model.pkl')
    joblib.dump(pipeline, model_path)
    
    metadata = {
        "model_type": "TFIDF_Char_LogisticRegression",
        "features": "Character N-Grams (3,5)",
        "metrics": {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1
        },
        "training_samples": len(X_train)
    }
    
    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Successfully saved model to {model_path}")

if __name__ == "__main__":
    main()
