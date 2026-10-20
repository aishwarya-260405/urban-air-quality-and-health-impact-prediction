"""
Exposure Engine

This module calculates the environmental exposure score
based on live AQI, forecast AQI, pollutants and weather.

Project:
Urban Air Quality Intelligence Platform
"""

from utils.who_rules import get_pollutant_status


# ==========================================================
# EXPOSURE SCORE CALCULATOR
# ==========================================================

def calculate_exposure(
        aqi,
        forecast_aqi,
        pm25,
        pm10,
        no2,
        so2,
        co,
        temperature,
        humidity,
        wind_speed
):

    score = 0

    reasons = []

    # ======================================================
    # AQI SCORE
    # ======================================================

    if aqi <= 50:
        score += 5
        reasons.append("Current AQI is Good.")

    elif aqi <= 100:
        score += 15
        reasons.append("Current AQI is Satisfactory.")

    elif aqi <= 200:
        score += 30
        reasons.append("Current AQI is Moderate.")

    elif aqi <= 300:
        score += 45
        reasons.append("Current AQI is Poor.")

    elif aqi <= 400:
        score += 60
        reasons.append("Current AQI is Very Poor.")

    else:
        score += 75
        reasons.append("Current AQI is Severe.")


    # ======================================================
    # FORECAST AQI
    # ======================================================

    if forecast_aqi > aqi:

        increase = forecast_aqi - aqi

        if increase >= 50:

            score += 15
            reasons.append("Forecast indicates pollution will increase significantly.")

        elif increase >= 20:

            score += 10
            reasons.append("Forecast indicates pollution will increase.")

        else:

            score += 5
            reasons.append("Forecast AQI is slightly higher.")

    else:

        reasons.append("Forecast indicates stable or improving air quality.")


    # ======================================================
    # PM2.5
    # ======================================================

    pm25_status = get_pollutant_status("PM2.5", pm25)

    score += pm25_status["score"]

    reasons.append(pm25_status["message"])


    # ======================================================
    # PM10
    # ======================================================

    pm10_status = get_pollutant_status("PM10", pm10)

    score += pm10_status["score"]

    reasons.append(pm10_status["message"])


    # ======================================================
    # NO2
    # ======================================================

    no2_status = get_pollutant_status("NO2", no2)

    score += no2_status["score"]

    reasons.append(no2_status["message"])


    # ======================================================
    # SO2
    # ======================================================

    so2_status = get_pollutant_status("SO2", so2)

    score += so2_status["score"]

    reasons.append(so2_status["message"])


    # ======================================================
    # CO
    # ======================================================

    co_status = get_pollutant_status("CO", co)

    score += co_status["score"]

    reasons.append(co_status["message"])


    # ======================================================
    # WEATHER MODIFIERS
    # ======================================================

    # High temperature

    if temperature >= 35:

        score += 5

        reasons.append("High temperature may worsen pollution effects.")


    # High humidity

    if humidity >= 80:

        score += 3

        reasons.append("High humidity may increase breathing discomfort.")


    # Low wind

    if wind_speed <= 2:

        score += 5

        reasons.append("Low wind speed may trap pollutants near ground level.")


    # Strong wind

    elif wind_speed >= 10:

        score -= 5

        reasons.append("Higher wind speed helps disperse pollutants.")


    # ======================================================
    # NORMALIZE SCORE
    # ======================================================

    score = max(0, min(score, 100))


    # ======================================================
    # EXPOSURE LEVEL
    # ======================================================

    if score <= 20:

        level = "Very Low"

    elif score <= 40:

        level = "Low"

    elif score <= 60:

        level = "Moderate"

    elif score <= 80:

        level = "High"

    else:

        level = "Very High"


    return {

        "score": score,

        "level": level,

        "reasons": reasons

    }