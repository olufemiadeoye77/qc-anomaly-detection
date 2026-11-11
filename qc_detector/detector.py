"""
Anomaly detection model wrapper for QC lab samples.
"""

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


class QCAnomalyDetector:
    """
    Wraps an Isolation Forest model for QC anomaly detection,
    with consistent fit/predict/save/load behavior.
    """

    def __init__(self, n_estimators: int = 200, contamination: float = 0.07, random_state: int = 42):
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
        )
        self.feature_cols = None

    def fit(self, X: pd.DataFrame):
        """Trains the model on the given feature data."""
        self.feature_cols = list(X.columns)
        self.model.fit(X)
        return self

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """Returns -1 for anomalies, 1 for normal samples."""
        return self.model.predict(X)

    def score(self, X: pd.DataFrame) -> pd.Series:
        """Returns anomaly scores (lower = more anomalous)."""
        return self.model.decision_function(X)

    def save(self, filepath: str):
        """Saves the trained model to disk."""
        joblib.dump(self, filepath)

    @staticmethod
    def load(filepath: str) -> "QCAnomalyDetector":
        """Loads a previously saved model."""
        return joblib.load(filepath)