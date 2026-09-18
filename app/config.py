from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("ENGIMIND_APP_NAME", "ENGI-MIND")
    version: str = os.getenv("ENGIMIND_VERSION", "0.1.0")
    environment: str = os.getenv("ENGIMIND_ENV", "development")

settings = Settings()
