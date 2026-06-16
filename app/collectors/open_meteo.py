import datetime as dt
import logging
from typing import Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.risk import classify_air_risk

logger = logging.getLogger(__name__)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _get(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()

def fetch_city_environment(city: dict[str, Any]) -> dict[str, Any]:
    lat = city["latitude"]
    lon = city["longitude"]
    weather = _get(WEATHER_URL, {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
    })
    air = _get(AIR_URL, {
        "latitude": lat,
        "longitude": lon,
        "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,european_aqi",
        "timezone": "auto",
    })

    current_weather = weather.get("current", {})
    current_air = air.get("current", {})
    observed_at = current_weather.get("time") or current_air.get("time") or dt.datetime.utcnow().isoformat()
    reading = {
        "city": city["name"],
        "latitude": lat,
        "longitude": lon,
        "observed_at": observed_at,
        "temperature_c": current_weather.get("temperature_2m"),
        "humidity_pct": current_weather.get("relative_humidity_2m"),
        "wind_speed_kmh": current_weather.get("wind_speed_10m"),
        "pm10": current_air.get("pm10"),
        "pm2_5": current_air.get("pm2_5"),
        "carbon_monoxide": current_air.get("carbon_monoxide"),
        "nitrogen_dioxide": current_air.get("nitrogen_dioxide"),
        "ozone": current_air.get("ozone"),
        "european_aqi": current_air.get("european_aqi"),
    }
    reading["risk_level"] = classify_air_risk(reading["pm2_5"], reading["pm10"], reading["european_aqi"])
    logger.info("Fetched %s risk=%s", reading["city"], reading["risk_level"])
    return reading
