"""Write 100 rows of the Telco Churn dataset to a remote database.

Connection settings are read from an env file (default: .env), never hardcoded.
See .env.example for the list of required variables.
"""

import argparse
import os
import re
from pathlib import Path

import polars as pl
from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    select,
)
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

ROOT = Path(__file__).resolve().parents[1]
PARQUET_PATH = ROOT / "data" / "processed" / "telco_churn.parquet"
N_ROWS = 100
SEED = 42
REQUIRED_VARS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "TABLE_NAME"]


def read_env(env_file: Path) -> dict[str, str]:
    """Load settings from the env file and validate them."""
    if not env_file.exists():
        raise SystemExit(f"Env file {env_file} not found. Copy .env.example first.")
    load_dotenv(env_file, override=True)
    missing = [name for name in REQUIRED_VARS if not os.getenv(name)]
    if missing:
        raise SystemExit(f"Missing variables in env file: {', '.join(missing)}")
    settings = {name: os.environ[name] for name in REQUIRED_VARS}
    settings["DB_DRIVER"] = os.getenv("DB_DRIVER", "postgresql+psycopg2")
    if not re.fullmatch(r"[a-z]+", settings["TABLE_NAME"]):
        raise SystemExit("TABLE_NAME must contain only lowercase latin letters.")
    return settings


def load_sample(path: Path = PARQUET_PATH, n: int = N_ROWS) -> pl.DataFrame:
    """Read the processed dataset and take a reproducible sample of n rows."""
    if not path.exists():
        raise SystemExit(f"{path} not found. Run `python src/data_loader.py` first.")
    df = pl.read_parquet(path).sample(n=n, seed=SEED)
    # Categorical columns are written as plain text
    return df.with_columns(pl.col(pl.Categorical).cast(pl.String))


def to_sa_type(dtype: pl.DataType):
    """Map a Polars dtype to a SQLAlchemy column type."""
    if dtype == pl.Boolean:
        return Boolean
    if dtype.is_integer():
        return Integer
    if dtype.is_float():
        return Float
    return String(255)


def write_table(df: pl.DataFrame, settings: dict[str, str], if_exists: str) -> int:
    """Create the table, insert the rows and return the stored row count."""
    url = URL.create(
        settings["DB_DRIVER"],
        username=settings["DB_USER"],
        password=settings["DB_PASSWORD"],
        host=settings["DB_HOST"],
        port=int(settings["DB_PORT"]),
        database=settings["DB_NAME"],
    )
    engine = create_engine(url)
    metadata = MetaData()
    table = Table(
        settings["TABLE_NAME"],
        metadata,
        *[Column(name, to_sa_type(dtype)) for name, dtype in df.schema.items()],
    )
    with engine.begin() as conn:
        if if_exists == "replace":
            table.drop(conn, checkfirst=True)
        table.create(conn)
        conn.execute(table.insert(), df.to_dicts())
        return conn.execute(select(func.count()).select_from(table)).scalar_one()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--if-exists", choices=["fail", "replace"], default="fail")
    args = parser.parse_args()

    settings = read_env(args.env_file)
    df = load_sample()
    try:
        count = write_table(df, settings, args.if_exists)
    except SQLAlchemyError as exc:
        raise SystemExit(f"Database error: {type(exc).__name__}") from None
    print(f"Done: table '{settings['TABLE_NAME']}' contains {count} rows.")


if __name__ == "__main__":
    main()
