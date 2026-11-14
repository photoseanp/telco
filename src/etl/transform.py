"""Transform step: clean values and cast columns to proper types."""

import logging

import polars as pl

log = logging.getLogger(__name__)

YES_NO_COLS = [
    "Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn",
]
CATEGORICAL_COLS = [
    "gender", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaymentMethod",
]


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """Strip strings, fix blank TotalCharges (new customers) and cast types."""
    df = df.with_columns(pl.col(pl.String).str.strip_chars())
    df = df.with_columns(
        pl.col("TotalCharges").replace("", None).cast(pl.Float64).fill_null(0.0),
        pl.col("MonthlyCharges").cast(pl.Float64),
        pl.col("tenure").cast(pl.Int32),
        (pl.col("SeniorCitizen") == "1").alias("SeniorCitizen"),
        *[(pl.col(c) == "Yes").alias(c) for c in YES_NO_COLS],
        *[pl.col(c).cast(pl.Categorical) for c in CATEGORICAL_COLS],
    )
    log.info("Transformed to %d rows x %d columns", df.height, df.width)
    return df
