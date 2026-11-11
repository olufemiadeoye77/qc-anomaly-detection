"""
Lightweight alerting layer: scans a new batch of QC samples
using the trained model and prints/logs clear alerts for any
flagged anomalies. Designed to be run after each sampling batch
(e.g., every 4 hours) in a real lab workflow.

Usage: python scripts/run_alert_check.py <path_to_new_data.xlsx>
"""

import sys
import os
from datetime import datetime

from qc_detector.data_loader import load_qc_data, get_feature_columns
from qc_detector.detector import QCAnomalyDetector

MODEL_PATH = "models/isolation_forest_qc_final.pkl"
ALERT_LOG_PATH = "reports/alert_log.txt"


def run_alert_check(data_path: str):
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: No trained model found at {MODEL_PATH}. Run the pipeline first.")
        sys.exit(1)

    print(f"Loading new batch: {data_path}")
    df = load_qc_data(data_path)
    feature_cols = get_feature_columns()

    detector = QCAnomalyDetector.load(MODEL_PATH)
    X = df[feature_cols]

    df = df.copy()
    df["pred"] = detector.predict(X)
    df["anomaly_score"] = detector.score(X)

    flagged = df[df["pred"] == -1].sort_values("anomaly_score")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n--- QC Alert Check: {timestamp} ---")
    print(f"Samples checked: {len(df)}")
    print(f"Anomalies flagged: {len(flagged)}")

    log_lines = [f"\n=== QC Alert Check: {timestamp} ===", f"Samples checked: {len(df)}", f"Anomalies flagged: {len(flagged)}"]

    if len(flagged) == 0:
        print("No anomalies detected. All samples within expected range.")
        log_lines.append("No anomalies detected.")
    else:
        print("\n⚠ FLAGGED SAMPLES (most anomalous first):")
        for _, row in flagged.iterrows():
            sample_id = row.get("sample_id", "UNKNOWN")
            score = row["anomaly_score"]
            print(f"  - {sample_id} | anomaly_score={score:.4f}")
            log_lines.append(f"  FLAGGED: {sample_id} | anomaly_score={score:.4f}")
        print("\nRecommend manual QC review of flagged samples before release.")
        log_lines.append("Recommend manual QC review before release.")

    with open(ALERT_LOG_PATH, "a") as f:
        f.write("\n".join(log_lines) + "\n")

    print(f"\nAlert log updated -> {ALERT_LOG_PATH}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_alert_check.py <path_to_new_data.xlsx>")
        sys.exit(1)

    run_alert_check(sys.argv[1])