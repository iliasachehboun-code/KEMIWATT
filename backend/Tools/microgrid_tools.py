# ===============================================================
# 🧠 Microgrid Tools – Built-in + Custom utilities
# ===============================================================

import os
import pandas as pd
import numpy as np
from datetime import datetime

# === AGNO Built-in Tools ===
from agno.tools.reasoning import ReasoningTools
from agno.tools.calculator import CalculatorTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools


# ===============================================================
# 🔧 Custom Microgrid Tools
# ===============================================================

def load_microgrid_data(file_path: str) -> pd.DataFrame:
    """
    Load raw microgrid data from CSV.
    Columns expected: timestamp, voltage, current, temperature, power, soc
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    return df


def validate_microgrid_schema(df: pd.DataFrame) -> bool:
    """
    Ensures the DataFrame has all required columns.
    """
    required = {"timestamp", "voltage", "current", "temperature", "power", "soc"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


def clean_microgrid_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans NaNs, duplicates, and ensures timestamps are consistent.
    """
    df = df.drop_duplicates()
    df = df.dropna(subset=["timestamp", "voltage", "current"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df[df["timestamp"].notnull()]
    df = df.sort_values("timestamp")
    return df.reset_index(drop=True)


def detect_outliers(df: pd.DataFrame, col: str, z_thresh: float = 3.0) -> pd.DataFrame:
    """
    Detect outliers in a column using Z-score method.
    """
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in dataset.")
    df["z_score"] = (df[col] - df[col].mean()) / df[col].std()
    return df[np.abs(df["z_score"]) > z_thresh]


def compute_efficiency(df: pd.DataFrame) -> float:
    """
    Compute energy efficiency = (avg power output / avg power input) * 100.
    """
    if "power" not in df.columns or "soc" not in df.columns:
        return np.nan
    power_output = df["power"].clip(lower=0).mean()
    power_input = np.abs(df["power"].clip(upper=0)).mean()
    if power_input == 0:
        return np.nan
    return round((power_output / power_input) * 100, 2)


def save_clean_data(df: pd.DataFrame, path: str) -> str:
    """
    Save cleaned data to a CSV file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return f"✅ Clean data saved to {path}"


def log_guardrail_event(log_path: str, message: str, level: str = "INFO"):
    """
    Save a guardrail or system event log entry.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] [{level}] {message}\n")


def generate_report_summary(df: pd.DataFrame) -> str:
    """
    Generates a quick Markdown summary of key metrics.
    """
    avg_power = df["power"].mean() if "power" in df else np.nan
    avg_temp = df["temperature"].mean() if "temperature" in df else np.nan
    avg_soc = df["soc"].mean() if "soc" in df else np.nan
    eff = compute_efficiency(df)

    return f"""
### ⚡ Microgrid Performance Summary
- Average Power: **{avg_power:.2f} kW**
- Average Temperature: **{avg_temp:.2f} °C**
- Average State of Charge: **{avg_soc:.2f} %**
- System Efficiency: **{eff:.2f} %**
"""


# ===============================================================
# ✅ Toolset Registry (for Agent imports)
# ===============================================================

BUILTIN_TOOLS = [
    ReasoningTools(),
    CalculatorTools(),
    DuckDuckGoTools(),
    FileTools()
]


CUSTOM_TOOLS = {
    "load_microgrid_data": load_microgrid_data,
    "validate_microgrid_schema": validate_microgrid_schema,
    "clean_microgrid_data": clean_microgrid_data,
    "detect_outliers": detect_outliers,
    "compute_efficiency": compute_efficiency,
    "save_clean_data": save_clean_data,
    "log_guardrail_event": log_guardrail_event,
    "generate_report_summary": generate_report_summary
}
