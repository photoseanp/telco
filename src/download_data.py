"""Download the Telco Customer Churn dataset from Kaggle.

Requires a Kaggle API token at ~/.kaggle/kaggle.json (see README.md).
"""

from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

DATASET = "blastchar/telco-customer-churn"
OUTPUT_DIR = Path("data/raw")


def download(dataset: str = DATASET, output_dir: Path = OUTPUT_DIR) -> None:
    """Download and unzip the dataset via the Kaggle API."""
    output_dir.mkdir(parents=True, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=str(output_dir), unzip=True)
    print(f"Dataset downloaded to {output_dir}")


if __name__ == "__main__":
    download()
