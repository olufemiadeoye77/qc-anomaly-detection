# QC Anomaly Detection — PKO/PKC Lab Samples

Prototype anomaly detection pipeline for palm kernel oil (PKO) and 
palm kernel cake (PKC) quality control lab results, built as part of 
a capstone on secure AI architecture for industrial operations.

## Pipeline

1. `scripts/generate_sample_data.py` — generates synthetic QC lab data
   (FFA%, moisture%, impurity%, iodine value, peroxide value)
2. `scripts/explore_data.py` — exploratory analysis and distribution plots
3. `scripts/train_anomaly_model.py` — trains an Isolation Forest model
4. `scripts/evaluate_model.py` — evaluates flagged anomalies, produces scatter plot

## Results (synthetic data, v1)

- Precision: 93.3%
- Recall: 93.3%
- 14/15 injected anomalies correctly flagged
- 1 missed anomaly, 1 additional legitimate low-end outlier caught

## Next steps

- Replace synthetic data with real LIMS export
- Tune contamination parameter and feature set
- Package as a reusable, importable module
- Add a simple reporting/alerting layer