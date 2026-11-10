# Telco Customer Churn Analysis

Exploratory data analysis of the **Telco Customer Churn** dataset, implemented in **Python** with **Polars**.
The project covers dataset download, loading, type casting, parquet export, a public-API data collection script,
an EDA notebook and a script that writes a dataset sample to a remote database.

## Dataset

- **Name:** Telco Customer Churn
- **Source:** Kaggle, published by BlastChar
- **Link:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **File:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Size:** 7,043 rows x 21 columns

The dataset describes customers of a telecom operator: account information (tenure, contract, payment method),
subscribed services (phone, internet, streaming, security add-ons), demographics and the target column `Churn` (Yes/No).
A column-by-column description is in [DATA.md](DATA.md).

### Downloading the dataset

1. Create a free Kaggle account and generate an API token (`Account -> Create New API Token`, saves `kaggle.json`).
2. Place `kaggle.json` in `~/.kaggle/kaggle.json` (`chmod 600` on Linux/macOS).
3. Activate the environment (see below) and run:

```bash
python src/download_data.py
```

The CSV is unpacked into `data/raw/`. Alternatively, download the file manually from the Kaggle page and place it at
`data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`.

## Environment Setup

Requires Python 3.11+ and `pip`.

```bash
# 1. Clone the repository and switch to the dev branch
git clone https://github.com/photoseanp/telco.git
cd telco
git checkout dev

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt            # runtime: polars, kaggle, requests, sqlalchemy, python-dotenv, psycopg2
pip install -r requirements-dev.txt        # notebook and tooling: jupyter, matplotlib, plotly, kaleido, ruff, ty
```

Static Plotly images (used in the notebook so that figures render on GitHub) require `kaleido` 1.x and a Chrome
installation. If Chrome is missing, run `plotly_get_chrome` once.

## Usage

### Data loader

```bash
python src/data_loader.py
```

The script reads the raw CSV, prints the first 10 rows, casts columns to proper types and saves the result to
`data/processed/telco_churn.parquet`.

Type casting (`cast_types`):
- `SeniorCitizen` and the Yes/No columns -> `Boolean`;
- `tenure` -> `Int32`; `MonthlyCharges`, `TotalCharges` -> `Float64`;
- service, contract, payment and gender columns -> `Categorical`;
- blank `TotalCharges` values (11 customers with `tenure = 0`, not billed yet) are filled with `0.0`.

Data files (`*.csv`, `*.parquet`, `data/`) are git-ignored and must not be committed.

### API data collection

```bash
python scripts/read_api.py
```

Builds a daily weather dataset from the free [Open-Meteo](https://open-meteo.com/en/docs) API. Details are in
[scripts/README.md](scripts/README.md). Note: the API may be unreachable from some regions without a VPN.

### EDA notebook

```bash
jupyter lab notebooks/EDA.ipynb
```

[notebooks/EDA.ipynb](notebooks/EDA.ipynb) covers data structure, completeness and integrity, outliers and anomalies,
metrics and distributions, correlations, extended Plotly visualizations, semantic analysis and conclusions.

Key results:
- 7,043 rows, one customer per row; `customerID` is unique.
- The only missing values are 11 `TotalCharges` entries (customers with `tenure = 0`).
- No outliers by the IQR rule; no logical inconsistencies between columns.
- Churn rate is 26.5 % (classes are imbalanced, about 3 : 1).
- Churn is highest for month-to-month contracts, fiber optic internet, electronic check payments and short tenure.
- `TotalCharges` is derived from `tenure x MonthlyCharges` (correlation with `tenure` is 0.83).

### Writing to the remote database

`scripts/write_to_db.py` writes a reproducible sample of 100 rows (`seed=42`) of the processed dataset to a table in a
remote database.

1. Prepare the processed dataset (see "Data loader").
2. Create an env file from the template and fill in the connection settings:

```bash
cp .env.example .env
```

Variables: `DB_DRIVER`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `TABLE_NAME`.
`TABLE_NAME` is the surname and initials in lowercase latin letters. If the database is not PostgreSQL, change
`DB_DRIVER` (for example `mysql+pymysql`) and install the matching driver.

3. Run the script:

```bash
python scripts/write_to_db.py                          # uses .env
python scripts/write_to_db.py --env-file .env.student  # another env file
python scripts/write_to_db.py --if-exists replace      # recreate the table
```

By default the script fails if the table already exists. On success it prints the number of rows stored in the table
(expected: 100).

The `.env*` files and database files are git-ignored. Credentials must never be committed, printed or hardcoded.

### Code quality

```bash
ruff format .
ruff check .
ty check
```

Ruff settings are defined in `pyproject.toml`.

## Project Structure

```
.
|-- README.md
|-- DATA.md                    # dataset description
|-- requirements.txt           # runtime dependencies
|-- requirements-dev.txt       # notebook and tooling dependencies
|-- pyproject.toml             # ruff configuration
|-- .env.example               # template of database settings (no real values)
|-- .gitignore
|-- notebooks/
|   |-- EDA.ipynb              # exploratory data analysis
|-- scripts/
|   |-- read_api.py            # builds a dataset from the Open-Meteo API
|   |-- write_to_db.py         # writes 100 dataset rows to a remote database
|   |-- README.md              # description of the API dataset
|-- src/
|   |-- download_data.py       # downloads the dataset from Kaggle
|   |-- data_loader.py         # loading, type casting, parquet export
|   |-- main.py                # short dataset summary
|-- data/                      # git-ignored contents
    |-- raw/                   # downloaded CSV
    |-- processed/             # parquet with typed data
```

## Tech Stack

- Python 3.11+
- [Polars](https://pola.rs/) for data processing
- matplotlib and [Plotly Express](https://plotly.com/python/plotly-express/) for visualization
- Kaggle API and `requests` for data collection
- SQLAlchemy and python-dotenv for database access
- Ruff and ty for formatting, linting and type checking
