"""
WHO Air Quality Guidelines (2021)

This module stores pollutant thresholds based on
World Health Organization (WHO) Air Quality Guidelines.

Project:
Urban Air Quality Intelligence Platform
"""

# ==========================================================
# WHO POLLUTANT GUIDELINES
# ==========================================================

WHO_LIMITS = {

    "PM2.5": {
        "safe": 15,
        "moderate": 35,
        "poor": 55,
        "very_poor": 100,
        "unit": "µg/m³"
    },

    "PM10": {
        "safe": 45,
        "moderate": 100,
        "poor": 150,
        "very_poor": 250,
        "unit": "µg/m³"
    },

    "NO2": {
        "safe": 25,
        "moderate": 50,
        "poor": 100,
        "very_poor": 200,
        "unit": "µg/m³"
    },

    "SO2": {
        "safe": 40,
        "moderate": 80,
        "poor": 150,
        "very_poor": 300,
        "unit": "µg/m³"
    },

    "CO": {
        "safe": 4,
        "moderate": 8,
        "poor": 12,
        "very_poor": 20,
        "unit": "mg/m³"
    },

    "O3": {
        "safe": 60,
        "moderate": 100,
        "poor": 150,
        "very_poor": 250,
        "unit": "µg/m³"
    }

}


# ==========================================================
# GET POLLUTANT STATUS
# ==========================================================

def get_pollutant_status(pollutant, value):

    pollutant = pollutant.upper()

    if pollutant not in WHO_LIMITS:
        return {
            "status": "Unknown",
            "score": 0,
            "message": "Pollutant not supported."
        }

    limits = WHO_LIMITS[pollutant]

    if value <= limits["safe"]:

        return {
            "status": "Safe",
            "score": 5,
            "message": f"{pollutant} is within WHO recommended limits."
        }

    elif value <= limits["moderate"]:

        return {
            "status": "Moderate",
            "score": 15,
            "message": f"{pollutant} is above the WHO safe limit."
        }

    elif value <= limits["poor"]:

        return {
            "status": "Poor",
            "score": 30,
            "message": f"{pollutant} concentration may affect sensitive individuals."
        }

    elif value <= limits["very_poor"]:

        return {
            "status": "Very Poor",
            "score": 45,
            "message": f"{pollutant} is at a harmful concentration."
        }

    else:

        return {
            "status": "Hazardous",
            "score": 60,
            "message": f"{pollutant} is at an extremely hazardous level."
        }