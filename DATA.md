# Dataset: Telco Customer Churn

## Source

- **Kaggle dataset:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **Author:** BlastChar
- **File name:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Shape:** 7,043 rows, 21 columns

The data itself is not stored in this repository (see `.gitignore`).

## How to obtain it

Run `python src/download_data.py` (uses the official Kaggle API) or download the CSV
manually from the link above and place it in `data/raw/`.

## Columns

| Column | Description |
|---|---|
| customerID | Unique customer identifier |
| gender | Customer gender (Male/Female) |
| SeniorCitizen | Whether the customer is a senior citizen (1/0) |
| Partner | Whether the customer has a partner (Yes/No) |
| Dependents | Whether the customer has dependents (Yes/No) |
| tenure | Number of months the customer has stayed with the company |
| PhoneService | Whether the customer has phone service (Yes/No) |
| MultipleLines | Whether the customer has multiple lines (Yes/No/No phone service) |
| InternetService | Customer's internet provider (DSL/Fiber optic/No) |
| OnlineSecurity | Whether the customer has online security add-on |
| OnlineBackup | Whether the customer has online backup add-on |
| DeviceProtection | Whether the customer has device protection add-on |
| TechSupport | Whether the customer has tech support add-on |
| StreamingTV | Whether the customer has streaming TV |
| StreamingMovies | Whether the customer has streaming movies |
| Contract | Contract term (Month-to-month/One year/Two year) |
| PaperlessBilling | Whether the customer uses paperless billing (Yes/No) |
| PaymentMethod | Payment method used |
| MonthlyCharges | Current monthly charge amount |
| TotalCharges | Total amount charged to the customer |
| Churn | Target: whether the customer churned (Yes/No) |
