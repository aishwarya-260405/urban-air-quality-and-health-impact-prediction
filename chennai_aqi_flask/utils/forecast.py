from utils.cpcb_rules import get_aqi_info
"""
Loads the deployed model bundle (trained by train_model.py, mirroring
Chennai_AQI_Full_Pipeline-2.ipynb Part 3) and produces a next-day AQI
forecast from a station's live 30-day history.

build_live_feature_row() mirrors the notebook's Part 3 cell 36 exactly,
including its fallback for WD2M / PRECTOTCORR, which aren't present in the
live Open-Meteo feed (only in the historical training CSV): WD2M defaults
to NaN, PRECTOTCORR defaults to 0.0 — same as the notebook, and the trained
RandomForestRegressor handles the NaN natively (scikit-learn's tree
ensembles support missing values).
"""

import os
import numpy as np
import pandas as pd
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "aqi_model.pkl")

MIN_DAYS_REQUIRED = 7  # need at least 7 days of live history for AQI_roll7 / AQI_lag7

_bundle = None
_load_attempted = False


def _load_bundle():
    global _bundle, _load_attempted
    if _load_attempted:
        return _bundle
    _load_attempted = True
    if os.path.exists(MODEL_PATH):
        try:
            _bundle = joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"[forecast] Found model file but failed to load it: {e}")
            _bundle = None
    return _bundle


def build_live_feature_row(history_df: pd.DataFrame, station: str, stations: list):
    """Mirrors notebook Part 3 cell 36's build_live_feature_row()."""
    g = history_df[history_df["Station"] == station].sort_values("Date").reset_index(drop=True)
    n = len(g)
    if n < MIN_DAYS_REQUIRED:
        return None, n

    latest = g.iloc[-1]
    row = {
        "AQI_today": latest["AQI Value"],
        "AQI_lag1": g["AQI Value"].iloc[-2],
        "AQI_lag2": g["AQI Value"].iloc[-3] if n >= 3 else g["AQI Value"].iloc[-2],
        "AQI_lag3": g["AQI Value"].iloc[-4] if n >= 4 else g["AQI Value"].iloc[-2],
        "AQI_lag7": g["AQI Value"].iloc[-8] if n >= 8 else g["AQI Value"].mean(),
        "AQI_roll3": g["AQI Value"].tail(3).mean(),
        "AQI_roll7": g["AQI Value"].tail(min(7, n)).mean(),
        "T2M_today": latest["T2M"],
        "RH2M_today": latest["RH2M"],
        "WS2M_today": latest["WS2M"],
        "WD2M_today": latest.get("WD2M", np.nan),
        "PRECTOTCORR_today": latest.get("PRECTOTCORR", 0.0),
        "PS_today": latest["PS"],
    }
    tomorrow = pd.to_datetime(latest["Date"]) + pd.Timedelta(days=1)
    row["target_dayofweek"] = tomorrow.dayofweek
    row["target_month"] = tomorrow.month
    row["target_is_weekend"] = int(tomorrow.dayofweek >= 5)
    for s in stations:
        row[f"st_{s}"] = 1 if s == station else 0

    return row, n

def explain_prediction(history_df: pd.DataFrame, station: str):
    """
    Generate a human-readable explanation for the AQI forecast.
    """

    g = history_df[
        history_df["Station"] == station
    ].sort_values("Date").reset_index(drop=True)

    if len(g) < 7:
        return {
            "summary": "Insufficient historical data for detailed AI explanation.",
            "reasons": [],
            "feature_importance": []
        }

    latest = g.iloc[-1]

    reasons = []

    # -------------------------------------------------
    # AQI Trend
    # -------------------------------------------------

    last3 = g["AQI Value"].tail(3).mean()
    last7 = g["AQI Value"].tail(7).mean()

    if last3 > last7:

        reasons.append(
            "Recent AQI trend is higher than the weekly average."
        )

    else:

        reasons.append(
            "Recent AQI remains close to the weekly average."
        )

    # -------------------------------------------------
    # Humidity
    # -------------------------------------------------

    if latest["RH2M"] > 75:

        reasons.append(
            "High humidity may reduce pollutant dispersion."
        )

    # -------------------------------------------------
    # Wind
    # -------------------------------------------------

    if latest["WS2M"] < 2:

        reasons.append(
            "Low wind speed may allow pollutants to accumulate."
        )

    else:

        reasons.append(
            "Moderate wind helps disperse pollutants."
        )

    # -------------------------------------------------
    # Temperature
    # -------------------------------------------------

    if latest["T2M"] > 34:

        reasons.append(
            "High temperature may influence ozone formation."
        )

    # -------------------------------------------------
    # Pressure
    # -------------------------------------------------

    if latest["PS"] > 100:

        reasons.append(
            "Stable atmospheric pressure supports current pollution conditions."
        )

    feature_importance = get_feature_importance()


    return {

        "summary":
        "The Random Forest model primarily relied on recent AQI history and weather conditions to estimate tomorrow's air quality.",

        "reasons": reasons,

        "feature_importance": feature_importance

    }


def forecast_next_day(history_df: pd.DataFrame, station: str):
    """
    Returns:
    (forecast_aqi, method, n_days, confidence)
    """

    bundle = _load_bundle()

    today_aqi = None

    if len(history_df):

        latest_row = history_df[
            history_df["Station"] == station
        ].sort_values("Date")

        if len(latest_row):

            today_aqi = latest_row.iloc[-1]["AQI Value"]

    # --------------------------------------------------
    # Use Random Forest Model
    # --------------------------------------------------

    if bundle is not None:

        row, n_days = build_live_feature_row(
            history_df,
            station,
            bundle["stations"]
        )

        if row is not None:

            try:

                X_live = pd.DataFrame([row])[bundle["feature_cols"]]

                pred = bundle["model"].predict(X_live)[0]

                pred = round(float(pred), 1)

                change = abs(pred - today_aqi)

                confidence = max(
                    75,
                    round(98 - change * 0.6)
                )

                print("TODAY =", today_aqi)
                print("PRED =", pred)
                print("CHANGE =", change)
                print("CONFIDENCE =", confidence)

                return (
                    pred,
                    "Random Forest",
                    n_days,
                    confidence
                )

            except Exception as e:

                print(f"[forecast] Model prediction failed: {e}")

                if today_aqi is not None:

                    return (
                    round(float(today_aqi), 1),
                    "Persistence",
                    n_days,
                    75
                )

            return (
                0,
                "Unavailable",
                n_days,
                0
            )

        else:

            if today_aqi is not None:

                return (
                    round(float(today_aqi), 1),
                    "persistence_insufficient_history",
                    n_days,
                    75
                )

            return (
                None,
                "insufficient_history",
                n_days,
                0
            )

            # --------------------------------------------------
    # Final fallback
    # --------------------------------------------------

    if today_aqi is not None:

        return (
            round(float(today_aqi), 1),
            "Persistence",
            0,
            75
        )

    return (
        0,
        "Unavailable",
        0,
        0
    )
def forecast_next_7_days(history_df, station):
    """
    Predict AQI for the next 7 days.
    Returns a list containing AQI, category, color and health message
    for each predicted day.
    """

    history = history_df.copy()

    history["Date"] = pd.to_datetime(history["Date"])

    forecast = []

    for i in range(1, 8):

        pred, method, _, _ = forecast_next_day(
            history,
            station
        )

        info = get_aqi_info(pred)

        forecast.append({

            "day": f"Day {i}",

            "aqi": round(pred),

            "category": info["category"],

            "color": info["color"],

            "message": info["health_message"]

        })

        # ----------------------------------------
        # Append predicted day for recursive forecast
        # ----------------------------------------

        latest = history[
            history["Station"] == station
        ].sort_values("Date").iloc[-1].copy()

        latest["Date"] = pd.to_datetime(
            latest["Date"]
        ) + pd.Timedelta(days=1)

        latest["AQI Value"] = pred

        history = pd.concat(

            [
                history,
                pd.DataFrame([latest])
            ],

            ignore_index=True

        )

    return forecast

# ==========================================================
# FEATURE IMPORTANCE (Explainable AI)
# ==========================================================

def get_feature_importance():

    bundle = _load_bundle()

    if bundle is None:
        return []

    model = bundle["model"]
    cols = bundle["feature_cols"]

    if not hasattr(model, "feature_importances_"):
        return []

    importance = []

    for feature, weight in zip(cols, model.feature_importances_):

        importance.append({

            "feature": feature,
            "weight": round(weight * 100, 1)

        })

    importance.sort(
        key=lambda x: x["weight"],
        reverse=True
    )

    feature_names = {

        "AQI_today": "Current AQI",
        "AQI_roll7": "Recent AQI Trend",
        "AQI_roll3": "Last 3-Day AQI",
        "AQI_lag1": "Yesterday AQI",
        "AQI_lag2": "2-Day AQI",
        "AQI_lag3": "3-Day AQI",
        "AQI_lag7": "Last Week AQI",
        "RH2M_today": "Humidity",
        "T2M_today": "Temperature",
        "WS2M_today": "Wind Speed",
        "PS_today": "Pressure",
        "PRECTOTCORR_today": "Rainfall",
        "WD2M_today": "Wind Direction"

    }

    for item in importance:

        item["feature"] = feature_names.get(
            item["feature"],
            item["feature"]
        )

    return importance[:5]