"""
Trains and saves the DEPLOYED model exactly as in Part 3, Step 1 of
Chennai_AQI_Full_Pipeline-2.ipynb (cell 34): a RandomForestRegressor on the
"reduced" feature set (AQI lags/rolling stats + weather-today + calendar +
station dummies), trained on the FULL historical dataset.

Run this once (from the project root):
    python train_model.py

It reads chennai_aqi_weather_merged.csv and writes models/aqi_model.pkl,
a dict bundle: {"model": ..., "feature_cols": [...], "stations": [...]}.
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

SOURCE_CSV = "chennai_aqi_weather_merged.csv"
OUTPUT_PATH = "models/aqi_model.pkl"

pollutant_cols = ["SO2", "NO2", "CO", "PM2.5", "PM10"]
weather_cols = ["T2M", "RH2M", "WS2M", "WD2M", "PRECTOTCORR", "PS"]


def clean_and_reindex(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = (df_raw.drop_duplicates(subset=["Date", "Station"])
                .sort_values(["Station", "Date"])
                .reset_index(drop=True))
    filled = []
    for station, g in df.groupby("Station"):
        g = g.set_index("Date").sort_index()
        full_idx = pd.date_range(g.index.min(), g.index.max(), freq="D")
        g = g.reindex(full_idx)
        g["Station"] = station
        num_cols = pollutant_cols + weather_cols + ["AQI Value"]
        g[num_cols] = g[num_cols].interpolate(method="linear", limit=3, limit_direction="both")
        filled.append(g)
    return pd.concat(filled).rename_axis("Date").reset_index()


def make_features(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values("Date").copy()
    g["AQI_today"] = g["AQI Value"]
    g["AQI_lag1"] = g["AQI Value"].shift(1)
    g["AQI_lag2"] = g["AQI Value"].shift(2)
    g["AQI_lag3"] = g["AQI Value"].shift(3)
    g["AQI_lag7"] = g["AQI Value"].shift(7)
    g["AQI_roll3"] = g["AQI Value"].rolling(3).mean()
    g["AQI_roll7"] = g["AQI Value"].rolling(7).mean()
    for c in weather_cols:
        g[f"{c}_today"] = g[c]
    tomorrow = g["Date"] + pd.Timedelta(days=1)
    g["target_dayofweek"] = tomorrow.dt.dayofweek
    g["target_month"] = tomorrow.dt.month
    g["target_is_weekend"] = (tomorrow.dt.dayofweek >= 5).astype(int)
    g["target_AQI_t_plus1"] = g["AQI Value"].shift(-1)
    return g


def main():
    df_raw = pd.read_csv(SOURCE_CSV, parse_dates=["Date"])
    print("Loaded:", df_raw.shape)

    df2 = clean_and_reindex(df_raw)

    df_feat = df2.groupby("Station", group_keys=True).apply(make_features, include_groups=False)
    df_feat = df_feat.reset_index(level=0).reset_index(drop=True)

    reduced_features = (
        ["AQI_today", "AQI_lag1", "AQI_lag2", "AQI_lag3", "AQI_lag7", "AQI_roll3", "AQI_roll7"]
        + [f"{c}_today" for c in weather_cols]
        + ["target_dayofweek", "target_month", "target_is_weekend"]
    )
    target_col = "target_AQI_t_plus1"

    model_df = df_feat.dropna(subset=reduced_features + [target_col]).copy()
    station_list = sorted(model_df["Station"].unique())
    model_df = pd.get_dummies(model_df, columns=["Station"], prefix="st")
    station_cols = [f"st_{s}" for s in station_list]
    feature_cols = reduced_features + station_cols

    rf_deploy = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1)
    rf_deploy.fit(model_df[feature_cols], model_df[target_col])
    print(f"Trained on {len(model_df)} rows across {len(station_list)} stations.")
    print(f"Feature count: {len(feature_cols)}")

    importances = pd.Series(rf_deploy.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nTop 10 feature importances:")
    print(importances.head(10))

    bundle = {
        "model": rf_deploy,
        "feature_cols": feature_cols,
        "stations": station_list,
        "reduced_features": reduced_features,
    }
    joblib.dump(bundle, OUTPUT_PATH)
    print(f"\nSaved deployed model bundle to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
