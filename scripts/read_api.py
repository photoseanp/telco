"""Query the Open-Meteo forecast API and build a daily weather dataset."""

from pathlib import Path

import polars as pl
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
OUTPUT_PATH = Path("data/processed/weather_forecast.parquet")
FORECAST_DAYS = 7

CITIES: dict[str, tuple[float, float]] = {
    "Moscow": (55.75, 37.62),
    "Saint Petersburg": (59.94, 30.31),
    "Novosibirsk": (55.03, 82.92),
    "Yekaterinburg": (56.84, 60.65),
    "Kazan": (55.79, 49.12),
    "Sochi": (43.60, 39.73),
    "Vladivostok": (43.12, 131.89),
    "London": (51.51, -0.13),
    "Paris": (48.86, 2.35),
    "Berlin": (52.52, 13.41),
    "New York": (40.71, -74.01),
    "Tokyo": (35.68, 139.69),
    "Sydney": (-33.87, 151.21),
    "Cairo": (30.04, 31.24),
    "Rio de Janeiro": (-22.91, -43.17),
}

DAILY_VARS = {
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "precipitation_mm",
    "wind_speed_10m_max": "wind_max_kmh",
}


def fetch_city(name: str, lat: float, lon: float) -> pl.DataFrame:
    """Request the daily forecast for one city and return it as a DataFrame."""
    params: dict[str, str | float | int] = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join(DAILY_VARS),
        "timezone": "auto",
        "forecast_days": FORECAST_DAYS,
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    daily = response.json()["daily"]
    return pl.DataFrame(daily).with_columns(
        pl.lit(name).alias("city"),
        pl.lit(lat).alias("latitude"),
        pl.lit(lon).alias("longitude"),
    )


def build_dataset() -> pl.DataFrame:
    """Query every city and return one typed DataFrame."""
    frames = [fetch_city(name, lat, lon) for name, (lat, lon) in CITIES.items()]
    return (
        pl.concat(frames)
        .rename(DAILY_VARS)
        .with_columns(
            pl.col("time").str.to_date().alias("date"),
            pl.col("city").cast(pl.Categorical),
            pl.col("latitude", "longitude").cast(pl.Float64),
            pl.col("^.*_(c|mm|kmh)$").cast(pl.Float64),
        )
        .select(
            "city",
            "latitude",
            "longitude",
            "date",
            "temp_max_c",
            "temp_min_c",
            "precipitation_mm",
            "wind_max_kmh",
        )
    )


def save_parquet(df: pl.DataFrame, path: Path = OUTPUT_PATH) -> None:
    """Write the dataset to parquet (git-ignored)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)


if __name__ == "__main__":
    dataset = build_dataset()
    with pl.Config(tbl_rows=20, tbl_cols=-1):
        print(dataset.head(20))
    print(dataset.schema)
    print(f"Rows: {dataset.height}")
    save_parquet(dataset)
    print(f"Saved to {OUTPUT_PATH}")
