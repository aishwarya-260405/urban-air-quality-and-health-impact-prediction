"""
Live data feed — mirrors Chennai_AQI_Full_Pipeline-2.ipynb Part 2 (cell 26)
exactly: pulls the last N days of hourly pollutant + daily weather data from
Open-Meteo (free, no signup) for a station, aggregates to daily, and computes
CPCB National AQI from raw concentrations via the same breakpoint table used
to build the training data.

Fetching `past_days=30` in a single call gives enough daily history to build
the lag/rolling features the deployed model expects (AQI_lag7, AQI_roll7,
etc.) without needing to run a persistent daily logger.
"""

import pandas as pd
import requests

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

STATIONS = {
    "Kodungaiyur": (13.140961, 80.248175),
    "Koyambedu":   (13.069400, 80.194800),
    "Perungudi":   (12.965400, 80.246100),
    "Royapuram":   (13.104030, 80.293660),
    "Manali":      (13.163610, 80.258560),
}

# CPCB National AQI sub-index breakpoints — same table as the notebook's live feed.
BREAKPOINTS = {
    "pm25": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200),
             (91, 120, 201, 300), (121, 250, 301, 400), (251, 500, 401, 500)],
    "pm10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200),
             (251, 350, 201, 300), (351, 430, 301, 400), (431, 600, 401, 500)],
    "no2":  [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200),
             (181, 280, 201, 300), (281, 400, 301, 400), (401, 600, 401, 500)],
    "so2":  [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200),
             (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 2000, 401, 500)],
    "co":   [(0, 1.0, 0, 50), (1.1, 2.0, 51, 100), (2.1, 10, 101, 200),
             (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 50, 401, 500)],
}


def sub_index(pollutant, conc):
    if pd.isna(conc):
        return None
    table = BREAKPOINTS[pollutant]
    for lo, hi, ilo, ihi in table:
        if lo <= conc <= hi:
            return ilo + (ihi - ilo) / (hi - lo) * (conc - lo)
    lo, hi, ilo, ihi = table[-1]
    if conc > hi:
        return ilo + (ihi - ilo) / (hi - lo) * (conc - lo)
    return None


def compute_aqi_row(row):
    subs = {
        "pm25": sub_index("pm25", row["pm2_5"]),
        "pm10": sub_index("pm10", row["pm10"]),
        "no2": sub_index("no2", row["nitrogen_dioxide"]),
        "so2": sub_index("so2", row["sulphur_dioxide"]),
        "co": sub_index("co", row["CO_mg_m3"]),
    }
    valid = {k: v for k, v in subs.items() if v is not None}
    if not valid:
        return pd.Series({"AQI Value": None})
    return pd.Series({"AQI Value": round(max(valid.values()))})


def fetch_air_quality(name, lat, lon, days_back=30):
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide",
        "past_days": days_back, "forecast_days": 1, "timezone": "Asia/Kolkata",
    }
    resp = requests.get(AIR_QUALITY_URL, params=params, timeout=30)
    resp.raise_for_status()
    h = resp.json()["hourly"]
    df = pd.DataFrame(h)
    df["Date"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d")
    daily = df.groupby("Date").mean(numeric_only=True).reset_index()
    daily["Station"] = name
    daily["CO_mg_m3"] = daily["carbon_monoxide"] / 1000.0
    return daily


def fetch_weather(name, lat, lon, days_back=30):
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_mean,surface_pressure_mean",
        "past_days": days_back, "forecast_days": 1, "timezone": "Asia/Kolkata",
    }
    resp = requests.get(WEATHER_URL, params=params, timeout=30)
    resp.raise_for_status()
    d = resp.json()["daily"]
    df = pd.DataFrame(d).rename(columns={"time": "Date"})
    df["Station"] = name
    return df


def get_station_history(station: str, days_back: int = 30) -> pd.DataFrame:
    """Returns a daily history DataFrame for one station, schema matching
    chennai_live_history.csv: Date, Station, AQI Value, T2M, RH2M, WS2M, PS,
    SO2, NO2, CO, PM2.5, PM10."""
    if station not in STATIONS:
        raise ValueError(f"Unknown station: {station}")
    lat, lon = STATIONS[station]

    aq = fetch_air_quality(station, lat, lon, days_back)
    aq = pd.concat([aq, aq.apply(compute_aqi_row, axis=1)], axis=1)
    wx = fetch_weather(station, lat, lon, days_back)
    merged = aq.merge(wx, on=["Date", "Station"], how="left")

    history = pd.DataFrame({
        "Date": merged["Date"],
        "Station": merged["Station"],
        "AQI Value": merged["AQI Value"],
        "T2M": merged["temperature_2m_mean"].round(1),
        "RH2M": merged["relative_humidity_2m_mean"].round(1),
        "WS2M": merged["wind_speed_10m_mean"].round(2),
        "PS": merged["surface_pressure_mean"].round(1),
        "SO2": merged["sulphur_dioxide"].round(1),
        "NO2": merged["nitrogen_dioxide"].round(1),
        "CO": merged["CO_mg_m3"].round(2),
        "PM2.5": merged["pm2_5"].round(1),
        "PM10": merged["pm10"].round(1),
    })
    # Drop today's row if it's incomplete (partial day of hourly data -> NaN AQI)
    history = history.dropna(subset=["AQI Value"]).reset_index(drop=True)

    # Safety net: Open-Meteo's forecast endpoints can still return a stray
    # future-dated row even with forecast_days=1 (e.g. due to timezone
    # rollover). Never trust a "today" that's actually in the future.
    today_ist = pd.Timestamp.now(tz="Asia/Kolkata").strftime("%Y-%m-%d")
    history = history[history["Date"] <= today_ist].reset_index(drop=True)

    return history
