"""
Personal Health Risk Engine

This module calculates the personalized health risk
using:

- Exposure Score
- Age
- Existing Disease
- Smoking Habit

Project:
Urban Air Quality Intelligence Platform
"""

from utils.exposure import calculate_exposure


# ==========================================================
# AGE WEIGHTS
# ==========================================================

AGE_WEIGHTS = {

    "child": 20,
    "teen": 8,
    "adult": 2,
    "middle_age": 10,
    "senior": 20

}


# ==========================================================
# DISEASE WEIGHTS
# ==========================================================

DISEASE_WEIGHTS = {

    "None": 0,

    "Asthma": 25,

    "COPD": 30,

    "Heart Disease": 25,

    "Diabetes": 15,

    "Hypertension": 15,

    "Pregnancy": 20

}


# ==========================================================
# SMOKING WEIGHTS
# ==========================================================

SMOKING_WEIGHTS = {

    "Never": 0,

    "Former": 5,

    "Occasional": 10,

    "Daily": 20

}


# ==========================================================
# AGE CATEGORY
# ==========================================================

def get_age_weight(age):

    if age <= 12:

        return AGE_WEIGHTS["child"]

    elif age <= 18:

        return AGE_WEIGHTS["teen"]

    elif age <= 40:

        return AGE_WEIGHTS["adult"]

    elif age <= 60:

        return AGE_WEIGHTS["middle_age"]

    else:

        return AGE_WEIGHTS["senior"]


# ==========================================================
# HEALTH RISK
# ==========================================================

def calculate_health_risk(
        age,
        disease,
        smoking,
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
):

    # -----------------------------------------
    # Environmental Exposure
    # -----------------------------------------

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

    score = exposure["score"]


    reasons = exposure["reasons"].copy()


    # -----------------------------------------
    # Age
    # -----------------------------------------

    age_weight = get_age_weight(age)

    score += age_weight

    reasons.append(f"Age contributes +{age_weight} risk points.")


    # -----------------------------------------
    # Disease
    # -----------------------------------------

    disease_weight = DISEASE_WEIGHTS.get(disease, 0)

    score += disease_weight

    if disease != "None":

        reasons.append(

            f"Existing condition ({disease}) increases health risk."

        )


    # -----------------------------------------
    # Smoking
    # -----------------------------------------

    smoking_weight = SMOKING_WEIGHTS.get(

        smoking,

        0

    )

    score += smoking_weight

    if smoking != "Never":

        reasons.append(

            f"Smoking habit contributes +{smoking_weight} risk points."

        )


    # -----------------------------------------
    # Normalize
    # -----------------------------------------

    score = min(score, 100)


    # -----------------------------------------
    # Final Risk
    # -----------------------------------------

    if score <= 20:

        risk = "Very Low"

        color = "#4CAF50"

    elif score <= 40:

        risk = "Low"

        color = "#8BC34A"

    elif score <= 60:

        risk = "Moderate"

        color = "#FDD835"

    elif score <= 80:

        risk = "High"

        color = "#FB8C00"

    else:

        risk = "Very High"

        color = "#E53935"


    return {

        "risk_score": score,

        "risk_level": risk,

        "color": color,

        "exposure_score": exposure["score"],

        "exposure_level": exposure["level"],

        "reasons": reasons

    }