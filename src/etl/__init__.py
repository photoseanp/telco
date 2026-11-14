"""ETL package for the Telco Customer Churn dataset.

Pipeline: extract (raw CSV) -> transform (clean, cast types) -> validate -> load (<=100 rows to a database).
"""

from etl.extract import extract
from etl.load import load
from etl.transform import transform
from etl.validate import validate

__all__ = ["extract", "transform", "validate", "load"]
