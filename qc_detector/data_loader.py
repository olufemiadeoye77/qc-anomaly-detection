"""
Data loading and validation for QC lab samples.
Supports both CSV (synthetic/test data) and Excel (real LIMS exports).
"""

import pandas as pd

# Maps your real LIMS column abbreviations to internal standard names
COLUMN_MAP = {
    "FFA": "ffa_percent",
    "MIV": "miv",
    "COLOUR": "colour",
    "PV": "peroxide_value",
    "SAP VALUE": "sap_value",
    "RI": "refractive_index",
    "S.G": "specific_gravity",
    "IV": "iodine_value",
}

REQUIRED_RAW_COLUMNS = list(COLUMN_MAP.keys())


def load_qc_data(filepath: str, sheet_name=0) -> pd.DataFrame:
    """
    Loads QC lab sample data from either a CSV or Excel file,
    standardizes column names, and validates required columns.

    Parameters
    ----------
    filepath : str
        Path to the .csv or .xlsx file.
    sheet_name : str or int, optional
        Sheet name or index, for Excel files with multiple sheets.

    Returns
    -------
    pd.DataFrame
        Validated QC sample data with standardized column names.

    Raises
    ------
    ValueError
        If required columns are missing, or file type is unsupported.
    """
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx") or filepath.endswith(".xls"):
        df = pd.read_excel(filepath, sheet_name=sheet_name)
    else:
        raise ValueError(f"Unsupported file type: {filepath}")

    missing_cols = set(REQUIRED_RAW_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.rename(columns=COLUMN_MAP)

    return df


def get_feature_columns() -> list:
    """Returns the list of standardized numeric feature columns used for modeling."""
    return list(COLUMN_MAP.values())