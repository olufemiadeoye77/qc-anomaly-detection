"""
Audit logging for model training and prediction runs.
Supports governance requirements: every run should be traceable
to a data source, model version, and timestamp.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = "reports/audit_log.jsonl"


def _file_hash(filepath: str) -> str:
    """Returns a short SHA-256 hash of a file's contents, for traceability."""
    try:
        with open(filepath, "rb") as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()[:16]
    except FileNotFoundError:
        return "FILE_NOT_FOUND"


def log_event(event_type: str, details: dict, log_path: str = AUDIT_LOG_PATH):
    """
    Appends a structured audit event to the audit log.

    Parameters
    ----------
    event_type : str
        e.g. "training_run", "prediction_run", "alert_check"
    details : dict
        Event-specific details (data path, model path, results, etc.)
    log_path : str
        Where to write the log (JSON Lines format, one event per line)
    """
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **details,
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_training_run(data_path: str, model_path: str, contamination: float, results: dict):
    """Logs a model training event with data/model traceability hashes."""
    log_event("training_run", {
        "data_path": data_path,
        "data_hash": _file_hash(data_path),
        "model_path": model_path,
        "contamination": contamination,
        "precision": results.get("precision"),
        "recall": results.get("recall"),
        "flagged_count": results.get("flagged_count"),
    })


def log_alert_check(data_path: str, model_path: str, samples_checked: int, anomalies_flagged: int):
    """Logs an alert check (prediction run on new data)."""
    log_event("alert_check", {
        "data_path": data_path,
        "data_hash": _file_hash(data_path),
        "model_path": model_path,
        "model_hash": _file_hash(model_path),
        "samples_checked": samples_checked,
        "anomalies_flagged": anomalies_flagged,
    })