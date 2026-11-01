"""Load the Telco Customer Churn dataset, fix column types and save to parquet."""

from pathlib import Path

import polars as pl

RAW_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PARQUET_PATH = Path("data/processed/telco_churn.parquet")

BOOL_COLS = [
    "SeniorCitizen", "Partner", "Dependents", "PhoneService",
    "PaperlessBilling", "Churn",
]
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
        # Blank TotalCharges (customers with tenure 0) -> null -> 0.0:
        # these customers have not been billed yet.
        pl.col("TotalCharges")
        .cast(pl.String)
        .str.strip_chars()
        .cast(pl.Float64, strict=False)
        .fill_null(0.0),
        pl.col("tenure").cast(pl.Int32),
        pl.col("MonthlyCharges").cast(pl.Float64),
        # SeniorCitizen is 0/1, the other flags are Yes/No
        (pl.col("SeniorCitizen") == 1).alias("SeniorCitizen"),
        *[(pl.col(c) == "Yes").alias(c) for c in BOOL_COLS if c != "SeniorCitizen"],
        *[pl.col(c).cast(pl.Categorical) for c in CATEGORICAL_COLS],
    )


def save_parquet(df: pl.DataFrame, path: Path = PARQUET_PATH) -> None:
    """Write the DataFrame to parquet (the file is git-ignored)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)


if __name__ == "__main__":
    raw = load_and_preview()
    typed = cast_types(raw)
    print(f"TotalCharges nulls in raw data: {raw['TotalCharges'].null_count()}")
    print(f"TotalCharges nulls after cast: {typed['TotalCharges'].null_count()}")
    print(typed.schema)
    save_parquet(typed)
    print(f"Saved to {PARQUET_PATH}")
