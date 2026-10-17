# scripts/

## read_api.py

Builds a small weather dataset from the free
[Open-Meteo Forecast API](https://open-meteo.com/en/docs) (no API key required).

- **Source:** `https://api.open-meteo.com/v1/forecast`
- **What is queried:** 7-day daily forecast for 15 cities (Russia, Europe, USA, Asia,
  Australia, Africa, South America), one request per city.
- **Fields:** city, latitude, longitude, date, `temp_max_c`, `temp_min_c`,
  `precipitation_mm`, `wind_max_kmh`.
- **Types:** `date` is `Date`, `city` is `Categorical`, all numeric columns are `Float64`.
- **Output:** `data/processed/weather_forecast.parquet` (git-ignored, not in the repo).

### Run

```bash
pip install -r requirements.txt
python scripts/read_api.py
```

### Check and format

```bash
pip install -r requirements-dev.txt
ruff format scripts
ruff check scripts
ty check scripts
```

### Dataset preview

![First 20 rows of the dataset](screenshot.png)
