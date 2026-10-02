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

> **Note:** the dataset is not stored in this repository. The `data/` folder and all
> `*.csv` / `*.zip` files are listed in `.gitignore`, so they are never committed.

### How to download the dataset

1. Create a free Kaggle account and generate an API token
   (`Account -> Create New API Token`, saves `kaggle.json`).
2. Place `kaggle.json` in `~/.kaggle/kaggle.json` (`chmod 600` on Linux/macOS).
3. Activate the environment (see below) and run:

```bash
python src/download_data.py
```

This uses the Kaggle API to fetch and unzip the dataset into `data/raw/`.

Alternatively, download the CSV manually from the Kaggle page above and place it at
`data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv` (create the folders with
`mkdir -p data/raw`).

## Environment Setup

Requires Python 3.11+ and `pip`.

```bash
# 1. Clone the repo and switch to the dev branch
git clone https://github.com/photoseanp/telco.git
cd telco
git checkout dev

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies from requirements.txt
pip install -r requirements.txt
```

## Running the Data Loader

```bash
python src/download_data.py   # downloads the CSV into data/raw/
python src/data_loader.py     # prints the first 10 rows of the dataset
```

## Project Structure

```
.
|-- README.md
|-- DATA.md
|-- requirements.txt
|-- .gitignore
|-- src/
|   |-- main.py            # loads and summarizes the dataset
|   |-- data_loader.py     # prints the first 10 rows
|   |-- download_data.py   # downloads the dataset from Kaggle
|-- data/
    |-- raw/               # dataset goes here (git-ignored, created locally)
```

## Tech Stack

- Python 3.11+
- [Polars](https://pola.rs/) for data processing
- Kaggle API for dataset download
