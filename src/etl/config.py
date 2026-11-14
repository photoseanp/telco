"""Paths and constants shared by the ETL modules."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

KAGGLE_DATASET = "blastchar/telco-customer-churn"
RAW_FILE = RAW_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
PROCESSED_FILE = PROCESSED_DIR / "telco_churn.parquet"

MAX_ROWS = 100
SEED = 42
