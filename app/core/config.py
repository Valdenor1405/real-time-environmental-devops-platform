from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    project_name: str = "Real-Time Environmental Intelligence DevOps Platform"
    database_url: str = Field(default="postgresql+psycopg2://devops:devops@postgres:5432/environment")
    redis_url: str = Field(default="redis://redis:6379/0")
    collector_interval_seconds: int = 60
    cities: str = "Fortaleza,-3.7319,-38.5267;Sao Paulo,-23.5505,-46.6333;Manaus,-3.1190,-60.0217;Rio de Janeiro,-22.9068,-43.1729;Recife,-8.0476,-34.8770"
    log_level: str = "INFO"

    @property
    def city_list(self) -> List[dict]:
        parsed = []
        for item in self.cities.split(";"):
            name, lat, lon = item.split(",")
            parsed.append({"name": name.strip(), "latitude": float(lat), "longitude": float(lon)})
        return parsed

settings = Settings()
