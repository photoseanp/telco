"""Load step: write a sample (max 100 rows) to a database and save parquet."""

import logging
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
    inspect,
    select,
)
from sqlalchemy.engine import URL, Engine

from etl.config import MAX_ROWS, PROCESSED_FILE, SEED

log = logging.getLogger(__name__)

_IDENTIFIER = re.compile(r"^[a-z_][a-z0-9_]*$")


def check_table_name(name: str) -> None:
    """Allow only lowercase latin identifiers as table names."""
    if not _IDENTIFIER.fullmatch(name):
        raise ValueError("Table name must match ^[a-z_][a-z0-9_]*$")


def save_parquet(df: pl.DataFrame, path: Path = PROCESSED_FILE) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)
    log.info("Saved parquet to %s", path)
    return path


def make_engine(env_file: str | None = None) -> Engine:
    """Build an engine from DB_* environment variables (never logged)."""
    if env_file:
        load_dotenv(env_file, override=True)
    names = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [n for n in names if not os.getenv(n)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {missing}")
    url = URL.create(
        drivername=os.getenv("DB_DRIVER", "postgresql+psycopg2"),
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    return create_engine(url)


def _sql_type(dtype: pl.DataType):
    if dtype == pl.Boolean:
        return Boolean
    if dtype.is_integer():
        return Integer
    if dtype.is_float():
        return Float
    return String


def load(
    df: pl.DataFrame,
    engine: Engine,
    table_name: str,
    max_rows: int = MAX_ROWS,
    if_exists: str = "fail",
) -> int:
    """Write at most `max_rows` random rows to `table_name`; return rows stored."""
    check_table_name(table_name)
    max_rows = min(max_rows, MAX_ROWS)
    sample = df.sample(n=min(max_rows, df.height), seed=SEED)
    sample = sample.with_columns(pl.col(pl.Categorical).cast(pl.String))

    meta = MetaData()
    table = Table(
        table_name,
        meta,
        *[Column(c, _sql_type(t)) for c, t in sample.schema.items()],
    )

    with engine.begin() as conn:
        if inspect(conn).has_table(table_name):
            if if_exists == "fail":
                raise RuntimeError(
                    f"Table '{table_name}' already exists (use --if-exists replace)"
                )
            table.drop(conn)
        table.create(conn)
        conn.execute(table.insert(), sample.to_dicts())
        count = conn.execute(select(func.count()).select_from(table)).scalar_one()
    log.info("Table '%s' contains %d rows", table_name, count)
    return count
