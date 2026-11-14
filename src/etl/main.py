"""CLI entry point: python -m etl.main --table <name> [options]."""

import argparse
import logging
import sys
from pathlib import Path

from etl.config import MAX_ROWS, RAW_FILE
from etl.extract import extract
from etl.load import load, make_engine, save_parquet
from etl.transform import transform
from etl.validate import ValidationError, validate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Telco churn ETL: extract -> transform -> validate -> load")
    p.add_argument("--table", required=True, help="target table name, e.g. berendeyaa")
    p.add_argument("--env-file", default=None, help="env file with DB_* settings (default: environment)")
    p.add_argument("--rows", type=int, default=MAX_ROWS, help=f"rows to load, max {MAX_ROWS}")
    p.add_argument("--if-exists", choices=["fail", "replace"], default="fail")
    p.add_argument("--input", default=str(RAW_FILE), help="path to the raw CSV")
    p.add_argument("--force-download", action="store_true", help="re-download the dataset from Kaggle")
    p.add_argument("--dry-run", action="store_true", help="run extract/transform/validate only, skip the DB")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    if not 1 <= args.rows <= MAX_ROWS:
        print(f"--rows must be between 1 and {MAX_ROWS}", file=sys.stderr)
        return 2
    try:
        df = extract(Path(args.input), force_download=args.force_download)
        df = validate(transform(df))
        save_parquet(df)
        if args.dry_run:
            print("Dry run finished: data is valid, database was not touched.")
            return 0
        count = load(df, make_engine(args.env_file), args.table, args.rows, args.if_exists)
    except ValidationError as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # keep credentials out of the output
        print(f"ETL failed: {type(e).__name__}", file=sys.stderr)
        return 1
    print(f"Done: table '{args.table}' contains {count} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
