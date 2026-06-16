CREATE TABLE IF NOT EXISTS environmental_readings (
    id SERIAL PRIMARY KEY,
    city VARCHAR(80) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_c DOUBLE PRECISION,
    humidity_pct DOUBLE PRECISION,
    wind_speed_kmh DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    pm2_5 DOUBLE PRECISION,
    carbon_monoxide DOUBLE PRECISION,
    nitrogen_dioxide DOUBLE PRECISION,
    ozone DOUBLE PRECISION,
    european_aqi DOUBLE PRECISION,
    risk_level VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_city_observed_at ON environmental_readings(city, observed_at DESC);
CREATE INDEX IF NOT EXISTS ix_risk_level ON environmental_readings(risk_level);
