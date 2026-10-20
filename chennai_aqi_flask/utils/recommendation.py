"""
==========================================================
Urban Air Quality Intelligence Platform
Recommendation Engine
==========================================================

This module generates:

• Weather Insights
• Pollutant Insights
• Forecast Insights
• Personal Recommendations
• Emergency Alerts
• Explainable AI
• Dynamic AI Recommendation Cards

Author : Aishwarya
"""

# ==========================================================
# Weather Intelligence
# ==========================================================

def weather_insight(
    temperature,
    humidity,
    wind_speed,
    current_aqi
):

    weather = []

    if temperature >= 35:

        weather.append({

            "title": "High Temperature",

            "message":
            "Hot weather can increase dehydration and respiratory discomfort."

        })

    elif temperature <= 18:

        weather.append({

            "title": "Cool Weather",

            "message":
            "Cool conditions may worsen breathing problems for sensitive people."

        })

    if humidity >= 75:

        weather.append({

            "title": "High Humidity",

            "message":
            "High humidity can trap pollutants close to the ground."

        })

    if wind_speed >= 15:

        weather.append({

            "title": "Strong Wind",

            "message":
            "Strong winds help disperse pollutants and improve air quality."

        })

    elif wind_speed <= 3:

        weather.append({

            "title": "Low Wind",

            "message":
            "Low wind allows pollutants to accumulate."

        })

    return weather


# ==========================================================
# Pollutant Intelligence
# ==========================================================

def pollutant_insight(

    pm25,
    pm10,
    no2,
    so2,
    co

):

    pollutants = []

    values = {

        "PM2.5": pm25,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co

    }

    primary = max(values, key=values.get)

    pollutants.append({

        "primary_pollutant": primary

    })

    for name, value in values.items():

        pollutants.append({

            "title": name,

            "message":
            f"{name} concentration is {value:.2f}."

        })

    return pollutants# ==========================================================
# Forecast Intelligence
# ==========================================================

def forecast_insight(

    current_aqi,
    forecast_aqi

):

    forecast = []

    difference = forecast_aqi - current_aqi

    if difference > 20:

        forecast.append({

            "title": "AQI Increasing",

            "message":
            "Air quality is expected to worsen significantly tomorrow."

        })

    elif difference > 5:

        forecast.append({

            "title": "AQI Slightly Increasing",

            "message":
            "Air quality may become slightly worse tomorrow."

        })

    elif difference < -20:

        forecast.append({

            "title": "AQI Improving",

            "message":
            "Air quality is expected to improve tomorrow."

        })

    else:

        forecast.append({

            "title": "Stable Forecast",

            "message":
            "No major AQI changes are expected tomorrow."

        })

    return forecast


# ==========================================================
# Personal Health Advisory
# ==========================================================

def personal_health_advisory(

    age,
    disease,
    smoking,

    current_aqi,
    forecast_aqi,

    exposure_level,
    risk_level

):

    advice = []

    disease = str(disease).lower()
    smoking = str(smoking).lower()

    if age < 18:

        advice.append({

            "message":
            "Children should reduce prolonged outdoor activities during polluted hours."

        })

    if age >= 60:

        advice.append({

            "message":
            "Senior citizens should avoid unnecessary outdoor exposure."

        })

    if disease == "asthma":

        advice.append({

            "message":
            "Carry your inhaler and avoid strenuous outdoor exercise."

        })

    elif disease == "copd":

        advice.append({

            "message":
            "Stay indoors whenever pollution levels rise."

        })

    elif disease == "heart disease":

        advice.append({

            "message":
            "Avoid heavy physical activity during poor air quality."

        })

    if smoking == "current":

        advice.append({

            "message":
            "Avoid smoking today because pollution increases lung damage."

        })

    if current_aqi >= 150:

        advice.append({

            "message":
            "Avoid unnecessary outdoor exposure until AQI improves."

        })

    return advice# ==========================================================
# Emergency Alerts
# ==========================================================

def emergency_alert(

    current_aqi,
    forecast_aqi,

    age,
    disease,
    smoking,

    risk_level

):

    alerts = []

    disease = str(disease).lower()

    if current_aqi >= 300:

        alerts.append({

            "title": "Health Emergency",

            "message":
            "AQI is hazardous. Everyone should remain indoors."

        })

    elif current_aqi >= 200:

        alerts.append({

            "title": "Very Poor Air Quality",

            "message":
            "Avoid all unnecessary outdoor activities."

        })

    if disease in ["asthma", "copd"] and current_aqi >= 150:

        alerts.append({

            "title": "Respiratory Alert",

            "message":
            "Use your prescribed medication and seek medical help if breathing worsens."

        })

    if age >= 60 and current_aqi >= 150:

        alerts.append({

            "title": "Senior Citizen Alert",

            "message":
            "Older adults should stay indoors today."

        })

    return alerts


# ==========================================================
# Explainable AI
# ==========================================================

def explainable_reasons(

    current_aqi,
    forecast_aqi,

    pm25,
    pm10,
    no2,
    so2,
    co,

    temperature,
    humidity,
    wind_speed,

    age,
    disease,
    smoking,

    risk_level

):

    reasons = []

    reasons.append(

        f"Current AQI is {current_aqi:.1f}."

    )

    if forecast_aqi - current_aqi >= 20:

        reasons.append(

            f"AI predicts AQI may increase to {forecast_aqi:.1f} tomorrow."

        )

    elif forecast_aqi < current_aqi:

        reasons.append(

            f"AI predicts AQI may improve to {forecast_aqi:.1f} tomorrow."

        )

    if disease.lower() != "none":

        reasons.append(

            f"Existing medical condition ({disease}) increases pollution sensitivity."

        )

    if smoking.lower() == "current":

        reasons.append(

            "Smoking increases respiratory health risks."

        )

    if age >= 60:

        reasons.append(

            "Older adults are more vulnerable to air pollution."

        )

    elif age <= 12:

        reasons.append(

            "Children are more sensitive to polluted air."

        )

    return reasons
# ==========================================================
# Dynamic AI Recommendation Cards
# ==========================================================

def build_dynamic_tip_cards(

    age,
    disease,
    smoking,

    current_aqi,
    forecast_aqi,

    primary_pollutant,

    exposure_level,
    risk_level

):

    cards = []

    disease = str(disease).strip().lower()
    smoking = str(smoking).strip().lower()

    # =====================================================
    # CHILD
    # =====================================================

    if age < 18:

        cards.append({

            "icon": "🧒",

            "title": "Child Protection",

            "message": "Children are more sensitive to air pollution. Reduce outdoor play during peak pollution hours."

        })

    # =====================================================
    # SENIOR
    # =====================================================

    elif age >= 60:

        cards.append({

            "icon": "👴",

            "title": "Senior Health",

            "message": "Older adults should avoid prolonged outdoor exposure and monitor breathing comfort."

        })

    # =====================================================
    # HEALTHY ADULT
    # =====================================================

    else:

        cards.append({

            "icon": "🌿",

            "title": "Healthy Lifestyle",

            "message": "Maintain regular exercise and monitor today's AQI before planning outdoor activities."

        })

    

    # =====================================================
    # ASTHMA
    # =====================================================

    if disease == "asthma":

        cards.append({

            "icon": "🫁",

            "title": "Asthma Care",

            "message": "Carry your inhaler and avoid outdoor exercise when pollution levels increase."

        })

    # =====================================================
    # COPD
    # =====================================================

    elif disease == "copd":

        cards.append({

            "icon": "🫁",

            "title": "Respiratory Protection",

            "message": "Stay indoors whenever possible and avoid polluted roads and traffic."

        })

    # =====================================================
    # HEART DISEASE
    # =====================================================

    elif disease == "heart disease":

        cards.append({

            "icon": "❤️",

            "title": "Heart Care",

            "message": "Avoid strenuous outdoor activities and monitor symptoms during poor air quality."

        })

        cards.append({

            "icon": "💊",

            "title": "Medication Reminder",

            "message": "Keep prescribed heart medication readily available throughout the day."

        })

    # =====================================================
    # DIABETES
    # =====================================================

    elif disease == "diabetes":

        cards.append({

            "icon": "🩸",

            "title": "Diabetes Care",

            "message": "Stay hydrated and avoid prolonged exposure to polluted outdoor environments."

        })

    # =====================================================
# NO DISEASE
# =====================================================

    elif disease == "none":

        cards.append({

        "icon": "💚",

        "title": "Preventive Care",

        "message": "Continue healthy habits and regularly monitor local AQI conditions."

    })

    # Healthy + Never Smoked

    if smoking == "never":

        cards.append({

            "icon": "🌿",

            "title": "Healthy Lifestyle",

            "message": "Continue your healthy lifestyle and monitor local AQI before outdoor activities."

        })

        if current_aqi <= 50:

            cards.append({

                "icon": "🏃",

                "title": "Outdoor Exercise",

                "message": "Today's air quality is suitable for walking, jogging and cycling."

            })

        elif current_aqi <= 100:

            cards.append({

                "icon": "🚶",

                "title": "Outdoor Activities",

                "message": "Outdoor activities are generally safe, but avoid heavy traffic areas."

            })

        else:

            cards.append({

                "icon": "😷",

                "title": "Reduce Exposure",

                "message": "Although you have no existing health conditions, reducing prolonged outdoor exposure is recommended today."

            })  

    

    # =====================================================
    # SMOKING STATUS
    # =====================================================

    if smoking == "current":

        cards.append({

            "icon": "🚭",

            "title": "Smoking Alert",

            "message": "Smoking combined with air pollution greatly increases lung and heart health risks. Avoid smoking today."

        })

    elif smoking == "former":

        cards.append({

            "icon": "🌱",

            "title": "Protect Your Lungs",

            "message": "Continue avoiding smoking and reduce exposure to polluted environments."

        })

    # =====================================================
    # AQI CATEGORY
    # =====================================================

    if current_aqi <= 50:

        if disease == "none":

            cards.append({

                "icon": "🏃",

                "title": "Outdoor Activities",

                "message": "Air quality is good today. Walking, jogging and cycling are safe."

            })

    elif current_aqi <= 100:

        cards.append({

            "icon": "🌤",

            "title": "Moderate Air Quality",

            "message": "Outdoor activities are acceptable, but avoid prolonged exposure near heavy traffic."

        })

    elif current_aqi <= 200:

        cards.append({

            "icon": "😷",

            "title": "Wear an N95 Mask",

            "message": "Sensitive individuals should wear an N95 mask and reduce outdoor exposure."

        })

    else:

        cards.append({

            "icon": "🚨",

            "title": "Stay Indoors",

            "message": "Air quality is unhealthy. Avoid unnecessary outdoor activities."

        })

    # =====================================================
    # FORECAST
    # =====================================================

    if forecast_aqi - current_aqi >= 20:

        cards.append({

            "icon": "📈",

            "title": "Tomorrow's Forecast",

            "message": "Air quality is expected to worsen significantly tomorrow. Plan outdoor work today."

        })

    elif current_aqi - forecast_aqi >= 20:

        cards.append({

            "icon": "🌈",

            "title": "Improving Air",

            "message": "Air quality is expected to improve tomorrow."

        })

    # =====================================================
    # PRIMARY POLLUTANT
    # =====================================================

    if current_aqi >= 100:

        if primary_pollutant == "PM2.5":

            cards.append({

                "icon": "🌫",

                "title": "PM2.5 Alert",

                "message": "Fine particulate matter is elevated. Limit prolonged outdoor exposure."

            })

        elif primary_pollutant == "PM10":

            cards.append({

                "icon": "🌪",

                "title": "Dust Alert",

                "message": "High dust levels detected. Avoid dusty roads and construction areas."

            })

        elif primary_pollutant == "NO2":

            cards.append({

                "icon": "🚗",

                "title": "Traffic Pollution",

                "message": "Nitrogen dioxide levels are elevated. Avoid heavy traffic routes."

            })

        elif primary_pollutant == "SO2":

            cards.append({

                "icon": "🏭",

                "title": "Industrial Pollution",

                "message": "Sulphur dioxide is elevated. Reduce exposure near industrial areas."

            })

        elif primary_pollutant == "CO":

            cards.append({

                "icon": "🔥",

                "title": "Carbon Monoxide",

                "message": "Avoid enclosed parking areas and locations with vehicle emissions."

            })    # =====================================================
    # SMART COMBINATION RULES
    # =====================================================

    # Child + Asthma
    if age < 18 and disease == "asthma":

        cards.insert(0,{

            "icon":"🚸",

            "title":"Child Asthma Protection",

            "message":"Avoid outdoor sports today and always carry prescribed asthma medication."

        })

    # Senior + Heart Disease
    elif age >= 60 and disease == "heart disease":

        cards.insert(0,{

            "icon":"❤️",

            "title":"High Cardiac Risk",

            "message":"Older adults with heart disease should minimize outdoor exposure and avoid physical exertion."

        })

    # Senior + COPD
    elif age >= 60 and disease == "copd":

        cards.insert(0,{

            "icon":"🫁",

            "title":"Respiratory Risk",

            "message":"Older adults with COPD should stay indoors during periods of poor air quality."

        })

    # Current Smoker + COPD
    if smoking == "current" and disease == "copd":

        cards.insert(0,{

            "icon":"🚭",

            "title":"Critical Lung Protection",

            "message":"Smoking together with COPD greatly increases breathing complications. Avoid smoking completely today."

        })

    # Current Smoker + Heart Disease
    if smoking == "current" and disease == "heart disease":

        cards.insert(0,{

            "icon":"❤️",

            "title":"Cardiac Protection",

            "message":"Smoking significantly increases cardiovascular stress. Avoid smoking and outdoor exertion."

        })

    # Current Smoker + Asthma
    if smoking == "current" and disease == "asthma":

        cards.insert(0,{

            "icon":"⚠️",

            "title":"Severe Asthma Risk",

            "message":"Smoking and asthma together greatly increase the chance of breathing difficulty."

        })

    # Healthy User
    if disease == "none" and smoking == "never" and age >= 18 and age < 60 and current_aqi <= 50:

        cards.insert(0,{

            "icon":"😊",

            "title":"Healthy Conditions",

            "message":"Current conditions are ideal for outdoor activities and maintaining your daily fitness routine."

        })

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique = []
    seen = set()

    for card in cards:

        if card["title"] not in seen:

            unique.append(card)

            seen.add(card["title"])

    cards = unique

    # =====================================================
    # SHOW ONLY TOP 4
    # =====================================================

    return cards[:4]

# ==========================================================
# Main Recommendation Engine
# ==========================================================

def generate_health_advisory(

    current_aqi,
    forecast_aqi,

    pm25,
    pm10,
    no2,
    so2,
    co,

    temperature,
    humidity,
    wind_speed,

    age,
    disease,
    smoking,

    exposure_level,
    risk_level

):

    # -------------------------------------------------
    # Weather
    # -------------------------------------------------

    weather = weather_insight(

        temperature,
        humidity,
        wind_speed,
        current_aqi

    )

    # -------------------------------------------------
    # Pollutants
    # -------------------------------------------------

    pollutants = pollutant_insight(

        pm25,
        pm10,
        no2,
        so2,
        co

    )

    # -------------------------------------------------
    # Forecast
    # -------------------------------------------------

    forecast = forecast_insight(

        current_aqi,
        forecast_aqi

    )

    # -------------------------------------------------
    # Personal Advisory
    # -------------------------------------------------

    personal = personal_health_advisory(

        age,
        disease,
        smoking,

        current_aqi,
        forecast_aqi,

        exposure_level,
        risk_level

    )

    # -------------------------------------------------
    # Emergency Alerts
    # -------------------------------------------------

    emergency = emergency_alert(

        current_aqi,
        forecast_aqi,

        age,
        disease,
        smoking,

        risk_level

    )

    # -------------------------------------------------
    # Explainable AI
    # -------------------------------------------------

    why = explainable_reasons(

        current_aqi,
        forecast_aqi,

        pm25,
        pm10,
        no2,
        so2,
        co,

        temperature,
        humidity,
        wind_speed,

        age,
        disease,
        smoking,

        risk_level

    )

    # -------------------------------------------------
    # Primary Pollutant
    # -------------------------------------------------

    primary = pollutants[0]["primary_pollutant"]

    # -------------------------------------------------
    # Dynamic Recommendation Cards
    # -------------------------------------------------

    tips = build_dynamic_tip_cards(

        age,
        disease,
        smoking,

        current_aqi,
        forecast_aqi,

        primary,

        exposure_level,
        risk_level

    )
        # =====================================================
    # ENSURE PERSONAL RECOMMENDATIONS ARE NEVER EMPTY
    # =====================================================

    if len(personal) == 0:

        if disease.lower() == "none":

            if current_aqi <= 50:

                personal.append({

                    "title": "Healthy Lifestyle",

                    "message": "Air quality is good today. Continue outdoor activities while maintaining your healthy lifestyle."

                })

            elif current_aqi <= 100:

                personal.append({

                    "title": "Moderate Air Quality",

                    "message": "You can continue normal activities, but avoid prolonged exposure near heavy traffic."

                })

            else:

                personal.append({

                    "title": "Reduce Outdoor Exposure",

                    "message": "Although you have no existing medical conditions, reducing prolonged outdoor exposure is recommended today."

                })

        else:

            personal.append({

                "title": "Daily Health Advice",

                "message": "Follow your prescribed treatment plan and continue monitoring local AQI before outdoor activities."

            })

    # ==========================================================
    # FINAL RESPONSE
    # ==========================================================

    return {

        "summary": {

            "current_aqi": round(current_aqi, 1),

            "forecast_aqi": round(forecast_aqi, 1),

            "primary_pollutant": primary,

            "risk_level": risk_level,

            "exposure_level": exposure_level

        },

        "weather": weather,

        "forecast": forecast,

        "pollutants": pollutants,

        "personal": personal,

        "tips": tips,

        "emergency": emergency,

        "why": why

    }