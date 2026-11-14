"""Extract step: obtain the raw CSV and read it into a DataFrame."""

import logging
from pathlib import Path

import polars as pl

from etl.config import KAGGLE_DATASET, RAW_DIR, RAW_FILE

log = logging.getLogger(__name__)


def download(dest: Path = RAW_DIR) -> None:
    """Download and unzip the dataset from Kaggle (needs ~/.kaggle/kaggle.json)."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    dest.mkdir(parents=True, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(KAGGLE_DATASET, path=str(dest), unzip=True)
    log.info("Dataset downloaded to %s", dest)


def extract(path: Path = RAW_FILE, force_download: bool = False) -> pl.DataFrame:
    """Return the raw dataset; download it first if the file is missing."""
    if force_download or not path.exists():
        download(path.parent)
    df = pl.read_csv(
        path, infer_schema_length=0
    )  # all columns as strings: types are cast in transform
    log.info("Extracted %d rows x %d columns from %s", df.height, df.width, path)
    return df
