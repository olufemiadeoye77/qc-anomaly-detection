"""
Tests for qc_detector.data_loader
"""

import pandas as pd
import pytest

from qc_detector.data_loader import load_qc_data, get_feature_columns, COLUMN_MAP


def test_get_feature_columns_returns_expected_count():
    cols = get_feature_columns()
    assert len(cols) == len(COLUMN_MAP)
    assert "ffa_percent" in cols
    assert "iodine_value" in cols


def test_load_qc_data_csv(tmp_path):
    # Create a minimal valid CSV matching required columns
    csv_path = tmp_path / "sample.csv"
    df = pd.DataFrame({
        "FFA": [0.1, 0.2],
        "MIV": [0.05, 0.06],
        "COLOUR": [2.5, 2.6],
        "PV": [1.5, 1.6],
        "SAP VALUE": [195, 196],
        "RI": [1.459, 1.460],
        "S.G": [0.915, 0.916],
        "IV": [18, 19],
    })
    df.to_csv(csv_path, index=False)

    result = load_qc_data(str(csv_path))

    assert "ffa_percent" in result.columns
    assert "iodine_value" in result.columns
    assert len(result) == 2


def test_load_qc_data_missing_columns_raises(tmp_path):
    csv_path = tmp_path / "bad_sample.csv"
    df = pd.DataFrame({"FFA": [0.1]})  # missing most required columns
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_qc_data(str(csv_path))


def test_load_qc_data_unsupported_filetype(tmp_path):
    bad_path = tmp_path / "sample.txt"
    bad_path.write_text("not real data")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_qc_data(str(bad_path))