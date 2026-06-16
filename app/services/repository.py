from datetime import datetime
from dateutil import parser
from sqlalchemy.orm import Session
from app.core.models import EnvironmentalReading

def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    return parser.parse(value)

def save_reading(db: Session, data: dict) -> EnvironmentalReading:
    record = EnvironmentalReading(**{**data, "observed_at": _parse_datetime(data["observed_at"])})
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def latest_readings(db: Session, limit: int = 100):
    return db.query(EnvironmentalReading).order_by(EnvironmentalReading.observed_at.desc()).limit(limit).all()

def latest_by_city(db: Session, city: str, limit: int = 50):
    return db.query(EnvironmentalReading).filter(EnvironmentalReading.city == city).order_by(EnvironmentalReading.observed_at.desc()).limit(limit).all()
