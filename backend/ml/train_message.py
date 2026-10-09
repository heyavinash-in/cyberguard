import os
import pandas as pd
import glob
import pickle
import json

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
DATASET_PATH = 'C:/Users/phoen/.cache/kagglehub/datasets/uciml/sms-spam-collection-dataset/versions/1/*.csv'

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    files = glob.glob(DATASET_PATH)
    if not files:
        print("Dataset not found!")
        return
        
    print(f"Loading dataset from {files[0]}...")
    df = pd.read_csv(files[0], encoding='latin-1')
    print(f"Dataset shape: {df.shape}")
    
    # Match the notebook's preprocessing steps exactly
    if 'v1' in df.columns and 'v2' in df.columns:
        df = df.rename(columns={"v1": "Category", "v2": "Text"})
    
    df['Category'] = df['Category'].map({'ham': 0, 'spam': 1})
    
    # Text and Label extraction
    df['Text'] = df['Text'].fillna('')
    X = df['Text'].values
    y = df['Category'].astype(int).values
    
    # 1. Train/Test Split (Important to split before TF-IDF to prevent data leakage)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Testing set: {len(X_test)} samples")
    
    # 2. TF-IDF Vectorization
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(max_features=15000, stop_words='english', ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Extracted {X_train_vec.shape[1]} features.")
    
    # 3. Train Models
    print("\nTraining Linear SVC (often >99% on text)...")
    model = LinearSVC(random_state=42, dual=False)
    model.fit(X_train_vec, y_train)
    
    # 4. Evaluate Model
    print("Evaluating model...")
    y_pred = model.predict(X_test_vec)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print("=== Evaluation Metrics ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"Confusion Matrix:\n{cm}")
    
    # 5. Save Model and Vectorizer
    print("\nSaving model and artifacts...")
    model_path = os.path.join(MODEL_DIR, 'spam_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    vectorizer_path = os.path.join(MODEL_DIR, 'spam_vectorizer.pkl')
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
        
    metadata = {
        "model_type": "LinearSVC_TFIDF",
        "max_features": 15000,
        "metrics": {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1
        }
    }
    
    with open(os.path.join(MODEL_DIR, 'spam_model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Successfully saved model to {model_path} and vectorizer to {vectorizer_path}")

if __name__ == "__main__":
    main()
