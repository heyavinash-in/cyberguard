import numpy as np
import os
import joblib
from typing import Dict, Any

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'account_isolation_forest.pkl')

class AccountAnomalyEngine:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                self.model = joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Failed to load Account Anomaly model: {e}")

    def evaluate(self, features: Dict[str, Any]) -> float:
        """
        Runs IsolationForest over boolean/numeric features.
        Returns a normalized anomaly score 0-100 where higher is more anomalous.
        """
        if not self.model:
            return 0.0

        # Vectorize features in the order trained
        feature_vector = [
            float(features["new_ip"]),
            float(features["new_country"]),
            float(features["new_device"]),
            float(features["unusual_login_hour"]),
            float(features["failed_login_count"]),
            float(features["mfa_configuration_changed"]),
            float(features["vpn_detected"]),
            float(features["multiple_active_sessions"]),
            float(features["impossible_travel"])
        ]

        try:
            # score_samples returns negative anomaly score. Lower values are more abnormal.
            # Convert to a 0-100 risk score
            score = self.model.score_samples(np.array([feature_vector]))[0]
            # Empirical normalization (approximate mapping for IF)
            normalized_score = max(0, min(100, int(((-score) - 0.3) * 200)))
            return float(normalized_score)
        except Exception:
            return 0.0
