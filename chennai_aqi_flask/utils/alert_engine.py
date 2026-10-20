"""
==========================================================
Alert Engine
==========================================================

This module acts as the central orchestrator of the
Urban Air Quality Intelligence Platform.

Responsibilities:
- Calculate environmental exposure
- Calculate personalized health risk
- Generate recommendations
- Combine everything into one clean response

Author: Aishwarya
Project:
Urban Air Quality Intelligence Platform
"""

from utils.exposure import calculate_exposure
from utils.risk_engine import calculate_health_risk
from utils.recommendation import generate_health_advisory


def generate_alert(data):
    """
    Generate a complete personalized air-quality report.

    Parameters
    ----------
    data : dict

        {
            "station": "...",

            "aqi": ...,
            "forecast_aqi": ...,

            "pm25": ...,
            "pm10": ...,
            "no2": ...,
            "so2": ...,
            "co": ...,

            "temperature": ...,
            "humidity": ...,
            "wind_speed": ...,

            "age": ...,
            "disease": "...",
            "smoking": "..."
        }

    Returns
    -------
    dict
    """

    # ==========================================================
    # Read Inputs
    # ==========================================================

    station = data.get("station", "Unknown")

    current_aqi = data.get("aqi", 0)
    forecast_aqi = data.get("forecast_aqi", current_aqi)

    pm25 = data.get("pm25", 0)
    pm10 = data.get("pm10", 0)
    no2 = data.get("no2", 0)
    so2 = data.get("so2", 0)
    co = data.get("co", 0)

    temperature = data.get("temperature", 25)
    humidity = data.get("humidity", 50)
    wind_speed = data.get("wind_speed", 3)

    age = data.get("age", 30)
    disease = data.get("disease", "None")
    smoking = data.get("smoking", "Never")

    # ==========================================================
    # Exposure Engine
    # ==========================================================

    exposure = calculate_exposure(
        current_aqi,
        forecast_aqi,
        pm25,
        pm10,
        no2,
        so2,
        co,
        temperature,
        humidity,
        wind_speed
    )

    # ==========================================================
    # Risk Engine
    # ==========================================================

    risk = calculate_health_risk(
        age=age,
        disease=disease,
        smoking=smoking,

        current_aqi=current_aqi,
        forecast_aqi=forecast_aqi,

        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        co=co,

        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed
    )

    # ==========================================================
    # Recommendation Engine
    # ==========================================================

    advisory = generate_health_advisory(

        current_aqi=current_aqi,
        forecast_aqi=forecast_aqi,

        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        co=co,

        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,

        age=age,
        disease=disease,
        smoking=smoking,

        exposure_level=exposure["level"],
        risk_level=risk["risk_level"]
    )

    # ==========================================================
    # AQI Trend
    # ==========================================================

    difference = forecast_aqi - current_aqi

    if difference > 15:
        trend = "Increasing"

    elif difference < -15:
        trend = "Decreasing"

    else:
        trend = "Stable"

    # ==========================================================
    # Final Response
    # ==========================================================

    return {

        "station": station,

        "summary": {

            "current_aqi": current_aqi,

            "forecast_aqi": forecast_aqi,

            "trend": trend,

            "risk_level": risk["risk_level"],

            "exposure_level": exposure["level"],

            "primary_pollutant":
                advisory["summary"]["primary_pollutant"]

},

        "exposure": exposure,

        "risk": risk,

        "advisory": advisory

    }