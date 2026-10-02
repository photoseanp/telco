"""Load the Telco Customer Churn dataset and print its first 10 rows."""

from pathlib import Path

import polars as pl

DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")


def load_and_preview(path: Path = DATA_PATH, n: int = 10) -> pl.DataFrame:
    """Read the CSV with Polars, print the first n rows and return the frame."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python src/download_data.py` first."
        )
    df = pl.read_csv(path)
    print(df.head(n))
    return df


if __name__ == "__main__":
    load_and_preview()
