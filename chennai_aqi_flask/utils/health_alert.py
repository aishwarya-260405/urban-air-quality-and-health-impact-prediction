"""
Personalized health-alert rules engine.
Ported 1:1 from the JS in chennai_aqi_health_alert.html (CPCB category table +
WHO/EPA sensitive-group guidance: sensitive individuals are alerted one
category earlier than the general public).
"""

# (low, high, label, rank, statement, color)
CATEGORY_TABLE = [
    (0, 50, "Good", 0, "Minimal impact.", "#4C9A5B"),
    (51, 100, "Satisfactory", 1,
     "May cause minor breathing discomfort to sensitive people.", "#9BB84A"),
    (101, 200, "Moderate", 2,
     "May cause breathing discomfort to people with lung disease such as "
     "asthma, and discomfort to people with heart disease, children, and "
     "older adults.", "#E0B93D"),
    (201, 300, "Poor", 3,
     "May cause breathing discomfort on prolonged exposure, and discomfort "
     "to people with heart disease.", "#E08A3D"),
    (301, 400, "Very Poor", 4,
     "May cause respiratory illness on prolonged exposure; effects more "
     "pronounced in people with lung and heart disease.", "#C9503F"),
    (401, 500, "Severe", 5,
     "May cause respiratory effects even in healthy people, and serious "
     "health impacts on people with lung/heart disease -- even during "
     "light activity.", "#7A2E3A"),
]

SENSITIVE_CONDITIONS = {"asthma", "copd", "cardiovascular", "pregnancy"}
GENERAL_ALERT_RANK = 3
SENSITIVE_ALERT_RANK = 2


def categorize(aqi: float) -> dict:
    for lo, hi, label, rank, statement, color in CATEGORY_TABLE:
        if lo <= aqi <= hi:
            return {"category": label, "rank": rank, "statement": statement, "color": color}
    # above 500 -> Severe
    lo, hi, label, rank, statement, color = CATEGORY_TABLE[-1]
    return {"category": label, "rank": rank, "statement": statement, "color": color}


def derive_profile_flags(age, conditions):
    cond_set = {c.lower() for c in conditions}
    is_child = age is not None and age < 12
    is_elderly = age is not None and age >= 60
    matched = sorted(cond_set & SENSITIVE_CONDITIONS)
    is_sensitive = is_child or is_elderly or bool(matched)

    labels = []
    if is_child:
        labels.append("child")
    if is_elderly:
        labels.append("elderly")
    labels.extend(matched)

    return {"isSensitive": is_sensitive, "labels": labels}


def get_personalized_alert(forecast_aqi, age, conditions, station):
    cat = categorize(forecast_aqi)
    profile = derive_profile_flags(age, conditions)
    threshold = SENSITIVE_ALERT_RANK if profile["isSensitive"] else GENERAL_ALERT_RANK
    should_alert = cat["rank"] >= threshold

    return {
        "station": station,
        "forecastAqi": forecast_aqi,
        "category": cat,
        "profile": profile,
        "shouldAlert": should_alert,
    }
