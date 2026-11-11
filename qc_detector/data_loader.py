"""
Data loading and validation for QC lab samples.
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "sample_id",
    "ffa_percent",
    "moisture_percent",
    "impurity_percent",
    "iodine_value",
    "peroxide_value",
]


def load_qc_data(filepath: str) -> pd.DataFrame:
    """
    Loads QC lab sample data from a CSV file and validates
    that required columns are present.

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing QC lab data.

    Returns
    -------
    pd.DataFrame
        Validated QC sample data.

    Raises
    ------
    ValueError
        If required columns are missing.
    """
    df = pd.read_csv(filepath)

    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    return df


def get_feature_columns() -> list:
    """Returns the list of numeric feature columns used for modeling."""
    return [c for c in REQUIRED_COLUMNS if c != "sample_id"]