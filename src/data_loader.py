"""Thin wrapper over the etl package: kept for backward compatibility."""

from etl.extract import extract
from etl.load import save_parquet
from etl.transform import transform

cast_types = transform

if __name__ == "__main__":
    raw = extract()
    print(raw.head(10))
    save_parquet(transform(raw))
