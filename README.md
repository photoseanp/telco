# Telco Customer Churn Analysis

## Project Description

This project analyzes the **Telco Customer Churn** dataset to explore customer behavior
patterns and build a foundation for predicting customer churn. The pipeline covers
data loading, cleaning, exploration, and preparation for downstream modeling,
implemented in **Python** using **Polars** for data processing.

## Dataset

- **Name:** Telco Customer Churn
- **Source:** Kaggle, published by BlastChar
- **Link:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **File:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Size:** 7,043 rows x 21 columns

The dataset contains customer account information (tenure, contract type, payment
method), services subscribed to (phone, internet, streaming, security add-ons),
demographic attributes, and the target column `Churn` (Yes/No).

See [DATA.md](DATA.md) for a full column-by-column description.

### How to download the dataset

1. Create a free Kaggle account and generate an API token
   (`Account -> Create New API Token`, saves `kaggle.json`).
2. Place `kaggle.json` in `~/.kaggle/kaggle.json` (`chmod 600` on Linux/macOS).
3. Install dependencies and download the dataset:

```bash
make install
make download-data
```

This runs `src/download_data.py`, which uses the Kaggle API to fetch and unzip the
dataset into `data/raw/`.

Alternatively, download the CSV manually from the Kaggle page above and place it at
`data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`.

## Project Structure

```
.
|-- README.md
|-- DATA.md
|-- requirements.txt
|-- Makefile
|-- .gitignore
|-- src/
|   |-- main.py            # entry point: loads and summarizes the dataset
|   |-- download_data.py   # downloads the dataset from Kaggle
|-- data/
    |-- raw/                # downloaded dataset (git-ignored)
```

## Setup

```bash
make install       # create venv and install dependencies
make download-data # download the dataset via Kaggle API
make run            # run the main pipeline
```

## Tech Stack

- Python 3.11+
- [Polars](https://pola.rs/) for data processing
- Kaggle API for dataset download
