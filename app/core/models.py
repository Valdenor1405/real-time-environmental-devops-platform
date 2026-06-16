from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.core.db import Base

class EnvironmentalReading(Base):
    __tablename__ = "environmental_readings"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(80), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    wind_speed_kmh = Column(Float)
    pm10 = Column(Float)
    pm2_5 = Column(Float)
    carbon_monoxide = Column(Float)
    nitrogen_dioxide = Column(Float)
    ozone = Column(Float)
    european_aqi = Column(Float)
    risk_level = Column(String(30), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

Index("ix_city_observed_at", EnvironmentalReading.city, EnvironmentalReading.observed_at.desc())
