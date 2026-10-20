from flask import Flask, render_template, request, jsonify

# ==========================================================
# IMPORT PROJECT MODULES
# ==========================================================

from utils.live_data import (
    STATIONS,
    get_station_history
)

from utils.forecast import (
    forecast_next_day,
    forecast_next_7_days,
    get_feature_importance,
    explain_prediction
)

from utils.cpcb_rules import (
    get_aqi_info
)

from utils.alert_engine import (
    generate_alert
)

# ==========================================================
# CREATE FLASK APP
# ==========================================================

app = Flask(__name__)

# ==========================================================
# HELPER FUNCTION
# ==========================================================

def _to_py(value):
    """
    Convert numpy/pandas values into native Python
    types for JSON serialization.
    """

    if value is None:
        return None

    try:
        import pandas as pd

        if pd.isna(value):
            return None

    except Exception:
        pass

    if hasattr(value, "item"):
        return value.item()

    return value


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        stations=list(STATIONS.keys())
    )


# ==========================================================
# DASHBOARD PAGE
# ==========================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        stations=list(STATIONS.keys())
    )


# ==========================================================
# FORECAST PAGE
# ==========================================================

@app.route("/forecast")
def forecast():

    return render_template(
        "forecast.html",
        stations=list(STATIONS.keys())
    )


# ==========================================================
# HEALTH PAGE
# ==========================================================

@app.route("/health")
def health():

    return render_template(
        "health.html",
        stations=list(STATIONS.keys())
    )


# ==========================================================
# ABOUT PAGE
# ==========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html",
        stations=list(STATIONS.keys())
    )
# ==========================================================
# LIVE AQI API
# ==========================================================

@app.route("/api/live/<station>")
def api_live(station):

    try:
        history = get_station_history(
            station,
            days_back=30
        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "error": f"Unable to fetch live AQI data: {e}"
        }), 500

    if history.empty:

        return jsonify({
            "error": "No live AQI data available."
        }), 404

    latest = history.iloc[-1]

    today_aqi = _to_py(
        latest["AQI Value"]
    )

    today_info = get_aqi_info(today_aqi)

    forecast_aqi, method, history_days, confidence = forecast_next_day(
    history,
    station
)

    feature_importance = get_feature_importance()

    next7 = forecast_next_7_days(
    history,
    station
)

    explanation = explain_prediction(
    history,
    station
)

    forecast_info = get_aqi_info(forecast_aqi)

    difference = forecast_aqi - today_aqi

    if difference > 15:
        trend = "Increasing"

    elif difference < -15:
        trend = "Decreasing"

    else:
        trend = "Stable"

    return jsonify({

        "station": station,

        "date": str(latest["Date"]),

        "history_days": int(history_days),

        "today_aqi": int(round(today_aqi)),

        "today_category": today_info["category"],

        "today_color": today_info["color"],

        "today_message": today_info["health_message"],

        "forecast_aqi": int(round(forecast_aqi)),

        "forecast_category": forecast_info["category"],

        "forecast_color": forecast_info["color"],

        "forecast_message": forecast_info["health_message"],

        "forecast_method": method,

        "confidence": confidence,

        "trend": trend,

        "pollutants": {

            "PM2.5": _to_py(latest["PM2.5"]),

            "PM10": _to_py(latest["PM10"]),

            "NO2": _to_py(latest["NO2"]),

            "SO2": _to_py(latest["SO2"]),

            "CO": _to_py(latest["CO"])

        },

        "weather": {

            "temperature": _to_py(latest["T2M"]),

            "humidity": _to_py(latest["RH2M"]),

            "wind_speed": _to_py(latest["WS2M"]),

            "pressure": _to_py(latest["PS"])

        },

        "ai_explanation": explanation,
        
        "next7": next7
        

    })
# ==========================================================
# PERSONALIZED HEALTH API
# ==========================================================

@app.route("/api/health", methods=["POST"])
def api_health():

    data = request.get_json(force=True)

    station = data.get("station")

    age = data.get("age")

    if age in ("", None):
        age = 25
    else:
        age = int(age)

    disease = data.get("disease", "None")

    smoking = data.get("smoking", "Never")

    try:

        history = get_station_history(
            station,
            days_back=30
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    if history.empty:

        return jsonify({
            "error": "No AQI data available."
        }), 404

    latest = history.iloc[-1]

    forecast_aqi, method, history_days, confidence = forecast_next_day(
    history,
    station
)

    payload = {

        "station": station,

        "aqi": float(latest["AQI Value"]),

        "forecast_aqi": float(forecast_aqi),

        "pm25": float(latest["PM2.5"]),

        "pm10": float(latest["PM10"]),

        "no2": float(latest["NO2"]),

        "so2": float(latest["SO2"]),

        "co": float(latest["CO"]),

        "temperature": float(latest["T2M"]),

        "humidity": float(latest["RH2M"]),

        "wind_speed": float(latest["WS2M"]),

        "age": age,

        "disease": disease,

        "smoking": smoking

    }

    report = generate_alert(payload)

    return jsonify(report)


# ==========================================================
# FORECAST API
# ==========================================================

@app.route("/api/forecast/<station>")
def api_forecast(station):

    try:

        history = get_station_history(
            station,
            days_back=30
        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "error": f"Forecast failed: {e}"
        }), 500

    if history.empty:

        return jsonify({
            "error": "No forecast data available."
        }), 404

    latest = history.iloc[-1]

    current_aqi = float(
        latest["AQI Value"]
    )

    # ---------------------------------------
    # Forecast
    # ---------------------------------------

    forecast_aqi, method, history_days, confidence = forecast_next_day(
        history,
        station
    )

    feature_importance = get_feature_importance()

    explanation = explain_prediction(
        history,
        station
    )

    forecast_info = get_aqi_info(
        forecast_aqi
    )

    change = round(
        forecast_aqi - current_aqi
    )

    if change > 15:

        trend = "Increasing"

    elif change < -15:

        trend = "Decreasing"

    else:

        trend = "Stable"

    return jsonify({

        "station": station,

        "today_aqi": int(round(current_aqi)),

        "forecast_aqi": int(round(forecast_aqi)),

        "difference": change,

        "trend": trend,

        "category": forecast_info["category"],

        "color": forecast_info["color"],

        "icon": forecast_info["icon"],

        "health_message": forecast_info["health_message"],

        "forecast_method": method,

        "confidence": confidence,

        "history_days": int(history_days),

        "feature_importance": feature_importance,

        "next7": next7,

        "explanation": explanation

    })

# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "500.html"
    ), 500


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )