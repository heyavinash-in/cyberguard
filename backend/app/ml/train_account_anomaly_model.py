import numpy as np
import os
import joblib
from sklearn.ensemble import IsolationForest

def train_and_save():
    # Synthetic dataset representing mostly normal behavior, with a few injected anomalies
    np.random.seed(42)
    
    # normal baseline
    # [new_ip, new_country, new_device, unusual_time, fail_count, mfa_change, vpn, multi_session, impossible_travel]
    normal_data = []
    for _ in range(1000):
        normal_data.append([
            np.random.choice([0, 1], p=[0.9, 0.1]),  # new_ip
            np.random.choice([0, 1], p=[0.98, 0.02]), # new_country
            np.random.choice([0, 1], p=[0.95, 0.05]), # new_device
            np.random.choice([0, 1], p=[0.8, 0.2]),  # unusual_time
            np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05]), # fail_count
            0, # mfa_change
            np.random.choice([0, 1], p=[0.8, 0.2]), # vpn
            np.random.choice([0, 1], p=[0.9, 0.1]), # multi_session
            0  # impossible_travel
        ])
        
    # Anomaly injection
    anomalies = [
        [1, 1, 1, 1, 5, 1, 0, 1, 1],
        [1, 1, 1, 0, 10, 0, 1, 0, 1],
        [0, 0, 1, 1, 0, 1, 0, 0, 0]
    ] * 5

    X = np.array(normal_data + anomalies)

    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    model.fit(X)

    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, 'account_isolation_forest.pkl')
    joblib.dump(model, model_path)
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_and_save()
