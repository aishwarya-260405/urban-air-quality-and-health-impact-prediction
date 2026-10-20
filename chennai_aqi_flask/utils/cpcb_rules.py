"""
CPCB Air Quality Index (AQI) Rules

This module provides official CPCB AQI categories,
colors, icons and health messages.
"""

# ==========================================================
# CPCB AQI CATEGORY RULES
# ==========================================================

CPCB_AQI_RULES = [

    {
        "min": 0,
        "max": 50,
        "category": "Good",
        "color": "#2ECC71",
        "icon": "🟢",
        "health_message": "Air quality is satisfactory and poses little or no health risk."
    },

    {
        "min": 51,
        "max": 100,
        "category": "Satisfactory",
        "color": "#8BC34A",
        "icon": "🟢",
        "health_message": "Minor breathing discomfort may occur in unusually sensitive individuals."
    },

    {
        "min": 101,
        "max": 200,
        "category": "Moderate",
        "color": "#FDD835",
        "icon": "🟡",
        "health_message": "Breathing discomfort may occur in people with lung disease, children and older adults."
    },

    {
        "min": 201,
        "max": 300,
        "category": "Poor",
        "color": "#FB8C00",
        "icon": "🟠",
        "health_message": "Breathing discomfort is likely on prolonged exposure, especially for sensitive groups."
    },

    {
        "min": 301,
        "max": 400,
        "category": "Very Poor",
        "color": "#E53935",
        "icon": "🔴",
        "health_message": "Respiratory illness may occur on prolonged exposure. Outdoor activity should be limited."
    },

    {
        "min": 401,
        "max": 500,
        "category": "Severe",
        "color": "#8E24AA",
        "icon": "🟣",
        "health_message": "Serious health effects are likely. Everyone should avoid prolonged outdoor exposure."
    }

]


# ==========================================================
# GET AQI INFORMATION
# ==========================================================

def get_aqi_info(aqi):
    """
    Returns CPCB AQI information for a given AQI value.
    """

    try:
        aqi = float(aqi)
    except (TypeError, ValueError):
        return {
            "category": "Unknown",
            "color": "#9E9E9E",
            "icon": "⚪",
            "health_message": "Invalid AQI value."
        }

    # Check AQI range
    for rule in CPCB_AQI_RULES:
        if rule["min"] <= aqi <= rule["max"]:
            return rule

    # Above CPCB range
    if aqi > 500:
        return {
            "category": "Severe",
            "color": "#8E24AA",
            "icon": "🟣",
            "health_message": "Hazardous air quality. Everyone should remain indoors and avoid all outdoor activities."
        }

    # Negative AQI
    return {
        "category": "Unknown",
        "color": "#9E9E9E",
        "icon": "⚪",
        "health_message": "AQI value is outside the supported range."
    }