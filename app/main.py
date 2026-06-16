from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import Base, engine, get_db
from app.services.repository import latest_by_city, latest_readings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.project_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "healthy", "project": settings.project_name}

@app.get("/cities")
def cities():
    return settings.city_list

@app.get("/readings/latest")
def get_latest(limit: int = 100, db: Session = Depends(get_db)):
    rows = latest_readings(db, limit)
    return [serialize(row) for row in rows]

@app.get("/readings/{city}")
def get_city(city: str, limit: int = 50, db: Session = Depends(get_db)):
    rows = latest_by_city(db, city, limit)
    return [serialize(row) for row in rows]

def serialize(row):
    return {
        "id": row.id,
        "city": row.city,
        "latitude": row.latitude,
        "longitude": row.longitude,
        "observed_at": row.observed_at.isoformat(),
        "temperature_c": row.temperature_c,
        "humidity_pct": row.humidity_pct,
        "wind_speed_kmh": row.wind_speed_kmh,
        "pm10": row.pm10,
        "pm2_5": row.pm2_5,
        "carbon_monoxide": row.carbon_monoxide,
        "nitrogen_dioxide": row.nitrogen_dioxide,
        "ozone": row.ozone,
        "european_aqi": row.european_aqi,
        "risk_level": row.risk_level,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }
