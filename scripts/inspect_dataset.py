import kagglehub
import pandas as pd
import os
import glob
import sys

def analyze():
    print("Downloading dataset...", flush=True)
    try:
        path = kagglehub.dataset_download("mdsultanulislamovi/phishing-website-detection-datasets")
        print("Path to dataset files:", path, flush=True)
    except Exception as e:
        print("Error downloading dataset:", e)
        sys.exit(1)

    csv_files = glob.glob(os.path.join(path, "*.csv"))
    print(f"Found {len(csv_files)} CSV files.", flush=True)

    for file in csv_files:
        print("="*80)
        print(f"File: {os.path.basename(file)}")
        try:
            df = pd.read_csv(file)
            print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            
            print("\n--- Columns ---")
            print(df.columns.tolist())
            
            print("\n--- Missing Values ---")
            missing = df.isnull().sum()
            print(missing[missing > 0].to_dict() if missing.sum() > 0 else "None")
            
            print("\n--- Duplicates ---")
            print(df.duplicated().sum())
            
            print("\n--- Possible Target Columns (Distribution) ---")
            possible_labels = [c for c in df.columns if any(kw in c.lower() for kw in ['label', 'class', 'target', 'status', 'result', 'type', 'phish'])]
            if possible_labels:
                for lc in possible_labels:
                    print(f"  {lc}: {df[lc].value_counts().to_dict()}")
            else:
                print("  Could not automatically detect label column.")
            
            print("\n--- Example Record ---")
            print(df.head(1).to_dict(orient='records')[0])
            print("="*80)
        except Exception as e:
            print("Error reading file:", e)

if __name__ == "__main__":
    analyze()
