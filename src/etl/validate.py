"""Validate step: fail fast if the transformed data breaks basic expectations."""

import logging

import polars as pl

log = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "customerID", "gender", "SeniorCitizen", "tenure", "MonthlyCharges",
    "TotalCharges", "Contract", "Churn",
}


class ValidationError(ValueError):
    """Raised when the dataset does not pass validation."""


def validate(df: pl.DataFrame) -> pl.DataFrame:
    """Run all checks, raise ValidationError with every problem found."""
    errors: list[str] = []

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValidationError(f"Missing columns: {sorted(missing)}")
    if df.is_empty():
        raise ValidationError("Dataset is empty")

    if df["customerID"].is_duplicated().any():
        errors.append("customerID contains duplicates")
    if df.null_count().sum_horizontal().item() > 0:
        errors.append("dataset contains null values")
    if (df["tenure"] < 0).any():
        errors.append("tenure has negative values")
    if (df["MonthlyCharges"] <= 0).any():
        errors.append("MonthlyCharges must be positive")
    if (df["TotalCharges"] < 0).any():
        errors.append("TotalCharges has negative values")

    if errors:
        raise ValidationError("; ".join(errors))
    log.info("Validation passed (%d rows)", df.height)
    return df
