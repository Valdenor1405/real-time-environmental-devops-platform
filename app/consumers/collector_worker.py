import logging
import time
from prometheus_client import Counter, Gauge, start_http_server
from app.collectors.open_meteo import fetch_city_environment
from app.core.config import settings
from app.core.db import Base, engine, SessionLocal
from app.services.repository import save_reading

logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("collector_worker")

READINGS_TOTAL = Counter("collector_readings_total", "Total readings collected", ["city", "risk"])
COLLECTOR_ERRORS = Counter("collector_errors_total", "Total collector errors", ["city"])
LAST_SUCCESS = Gauge("collector_last_success_timestamp", "Unix timestamp of last successful collection", ["city"])

def run_forever():
    Base.metadata.create_all(bind=engine)
    start_http_server(9101)
    logger.info("Collector started. Interval=%ss Cities=%s", settings.collector_interval_seconds, [c["name"] for c in settings.city_list])
    while True:
        for city in settings.city_list:
            db = SessionLocal()
            try:
                reading = fetch_city_environment(city)
                save_reading(db, reading)
                READINGS_TOTAL.labels(city=city["name"], risk=reading["risk_level"]).inc()
                LAST_SUCCESS.labels(city=city["name"]).set_to_current_time()
            except Exception:
                COLLECTOR_ERRORS.labels(city=city["name"]).inc()
                logger.exception("Failed collecting city=%s", city["name"])
            finally:
                db.close()
        time.sleep(settings.collector_interval_seconds)

if __name__ == "__main__":
    run_forever()
