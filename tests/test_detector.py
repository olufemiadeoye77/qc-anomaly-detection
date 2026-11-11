"""
Tests for qc_detector.detector
"""

import pandas as pd
import numpy as np

from qc_detector.detector import QCAnomalyDetector


def _make_sample_data():
    np.random.seed(0)
    return pd.DataFrame({
        "ffa_percent": np.random.normal(0.1, 0.02, 100),
        "peroxide_value": np.random.normal(1.5, 0.3, 100),
    })


def test_fit_predict_returns_valid_labels():
    X = _make_sample_data()
    detector = QCAnomalyDetector(contamination=0.05, random_state=0)
    detector.fit(X)
    preds = detector.predict(X)

    assert set(preds).issubset({-1, 1})
    assert len(preds) == len(X)


def test_score_returns_numeric_values():
    X = _make_sample_data()
    detector = QCAnomalyDetector(contamination=0.05, random_state=0)
    detector.fit(X)
    scores = detector.score(X)

    assert len(scores) == len(X)
    assert all(isinstance(s, (int, float, np.floating)) for s in scores)


def test_save_and_load_roundtrip(tmp_path):
    X = _make_sample_data()
    detector = QCAnomalyDetector(contamination=0.05, random_state=0)
    detector.fit(X)

    save_path = tmp_path / "model.pkl"
    detector.save(str(save_path))

    loaded = QCAnomalyDetector.load(str(save_path))
    original_preds = detector.predict(X)
    loaded_preds = loaded.predict(X)

    assert list(original_preds) == list(loaded_preds)