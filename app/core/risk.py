def classify_air_risk(pm2_5: float | None, pm10: float | None, aqi: float | None) -> str:
    """Simple recruiter-friendly risk model based on EU AQI/particulate thresholds."""
    score = max([v for v in [pm2_5, pm10, aqi] if v is not None] or [0])
    if score >= 100:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 35:
        return "MODERATE"
    return "LOW"
