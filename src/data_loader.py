"""Load the Telco Customer Churn dataset, fix column types and save to parquet."""

from pathlib import Path

import polars as pl

RAW_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PARQUET_PATH = Path("data/processed/telco_churn.parquet")

BOOL_COLS = ["Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn"]
CATEGORICAL_COLS = [
    "gender", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaymentMethod",
]


def read_csv(path: Path = RAW_PATH) -> pl.DataFrame:
    """Read the raw CSV with Polars."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python src/download_data.py` first."
        )
    return pl.read_csv(path)


def load_and_preview(path: Path = RAW_PATH, n: int = 10) -> pl.DataFrame:
    """Read the CSV, print the first n rows and return the frame."""
    df = read_csv(path)
    print(df.head(n))
    return df


def cast_types(df: pl.DataFrame) -> pl.DataFrame:
    """Return a DataFrame with proper dtypes."""
    return df.with_columns(
        # TotalCharges holds blank strings for new customers -> null
        pl.col("TotalCharges")
        .cast(pl.String)
        .str.strip_chars()
        .cast(pl.Float64, strict=False),
        pl.col("SeniorCitizen").cast(pl.Boolean),
        pl.col("tenure").cast(pl.Int32),
        pl.col("MonthlyCharges").cast(pl.Float64),
        *[(pl.col(c) == "Yes").alias(c) for c in BOOL_COLS],
        *[pl.col(c).cast(pl.Categorical) for c in CATEGORICAL_COLS],
    )


def save_parquet(df: pl.DataFrame, path: Path = PARQUET_PATH) -> None:
    """Write the DataFrame to parquet (the file is git-ignored)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)


if __name__ == "__main__":
    raw = load_and_preview()
    typed = cast_types(raw)
    print(typed.schema)
    save_parquet(typed)
    print(f"Saved to {PARQUET_PATH}")
