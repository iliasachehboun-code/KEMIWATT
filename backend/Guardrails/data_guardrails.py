import pandas as pd

NUMERIC_COLS = ["solar_output_kW", "consumption_kW", "battery_level", "voltage", "temperature"]

EXPECTED_RANGES = {
    "solar_output_kW": (0, 10000),      # kW (demo wide bounds)
    "consumption_kW":  (0, 10000),
    "battery_level":   (0, 100),        # %
    "voltage":         (30, 60),        # V (typical stack range for demo)
    "temperature":     (-20, 60),       # °C safe envelope
}

def validate_schema(df: pd.DataFrame):
    missing = [c for c in ["timestamp"] + NUMERIC_COLS if c not in df.columns]
    return ["❌ Missing required column(s): " + ", ".join(missing)] if missing else []

def validate_nulls(df: pd.DataFrame):
    issues = []
    if df["timestamp"].isnull().any():
        issues.append("❌ Null timestamps detected.")
    for c in NUMERIC_COLS:
        if df[c].isnull().any():
            issues.append(f"❌ Null values detected in column `{c}`.")
    return issues

def validate_negatives(df: pd.DataFrame):
    issues = []
    for c in NUMERIC_COLS:
        if (df[c] < 0).any():
            issues.append(f"❌ Negative values found in `{c}`.")
    return issues

def validate_ranges(df: pd.DataFrame):
    issues = []
    for c, (lo, hi) in EXPECTED_RANGES.items():
        if ((df[c] < lo) | (df[c] > hi)).any():
            issues.append(f"⚠️ `{c}` outside expected range [{lo}, {hi}].")
    return issues

def validate_data(df: pd.DataFrame):
    """Run all validations. Return dict with status and issues list."""
    errors = []
    errors += validate_schema(df)
    if errors:
        return {"status": "failed", "issues": errors}

    errors += validate_nulls(df)
    errors += validate_negatives(df)
    errors += validate_ranges(df)

    return {"status": "failed", "issues": errors} if errors else {"status": "passed", "issues": []}
