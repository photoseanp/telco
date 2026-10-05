"""Entry point: load the Telco Customer Churn dataset and print a summary."""

from pathlib import Path

import polars as pl

DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")


def load_data(path: Path = DATA_PATH) -> pl.DataFrame:
    """Load the dataset into a Polars DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run `python src/download_data.py` first.")
    return pl.read_csv(path)


def main() -> None:
    df = load_data()
    print(f"Rows: {df.height}, Columns: {df.width}")
    print(df.describe())


if __name__ == "__main__":
    main()
