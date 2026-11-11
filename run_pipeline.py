"""
Main pipeline: loads QC data (LIMS Excel format), trains the anomaly
detector, evaluates against the Pass/Fail label, and saves results.

Run with: python run_pipeline.py
"""

from sklearn.model_selection import train_test_split

from qc_detector.data_loader import load_qc_data, get_feature_columns
from qc_detector.detector import QCAnomalyDetector
from qc_detector.evaluator import evaluate_predictions

# --- Config ---
DATA_PATH = "data/qc_lims_sample.xlsx"
MODEL_OUTPUT_PATH = "models/isolation_forest_qc_final.pkl"
RESULTS_OUTPUT_PATH = "reports/qc_pipeline_results.csv"
TEST_SIZE = 0.3
RANDOM_STATE = 42
CONTAMINATION = 0.07


def main():
    print("Loading data...")
    df = load_qc_data(DATA_PATH)
    feature_cols = get_feature_columns()

    df["is_true_anomaly"] = df["pass_fail"] == "Fail"

    print("Splitting train/test...")
    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=df["is_true_anomaly"]
    )

    X_train = train_df[feature_cols]
    X_test = test_df[feature_cols]

    print("Training model...")
    detector = QCAnomalyDetector(contamination=CONTAMINATION, random_state=RANDOM_STATE)
    detector.fit(X_train)

    print("Scoring test set...")
    test_df = test_df.copy()
    test_df["pred"] = detector.predict(X_test)
    test_df["anomaly_score"] = detector.score(X_test)

    results = evaluate_predictions(test_df, true_label_col="is_true_anomaly", pred_col="pred")

    print("\n--- Results ---")
    print(f"Flagged: {results['flagged_count']}")
    print(f"True positives: {results['true_positives']}")
    print(f"False positives: {results['false_positives']} -> {results['false_positive_ids']}")
    print(f"False negatives: {results['false_negatives']} -> {results['false_negative_ids']}")
    print(f"Precision: {results['precision']:.2%}")
    print(f"Recall: {results['recall']:.2%}")

    detector.save(MODEL_OUTPUT_PATH)
    test_df.to_csv(RESULTS_OUTPUT_PATH, index=False)

    print(f"\nModel saved -> {MODEL_OUTPUT_PATH}")
    print(f"Results saved -> {RESULTS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()