import pandas as pd
import glob
import os

path = 'C:/Users/phoen/.cache/kagglehub/datasets/mdsultanulislamovi/phishing-website-detection-datasets/versions/1'
files = sorted(glob.glob(os.path.join(path, '*.csv')))

for f in files:
    try:
        df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip', encoding_errors='ignore')
        print(f"\n--- {os.path.basename(f)} ---")
        print(f"Shape: {df.shape}")
        
        # Determine likely label
        label_col = None
        for col in df.columns:
            c = col.lower()
            if c in ['label', 'class', 'target', 'status', 'result', 'type', 'class_label', 'phishing']:
                label_col = col
                break
        
        if label_col:
            print(f"Target Column: {label_col}")
            counts = df[label_col].value_counts().to_dict()
            print(f"Distribution: {counts}")
        else:
            print("Target Column: Not automatically found")
            print("Columns:", df.columns.tolist()[:10], "... (total", len(df.columns), ")")
            
        print("Missing Values:", df.isnull().sum().sum())
    except Exception as e:
        print(f"Failed to process {f}: {e}")
