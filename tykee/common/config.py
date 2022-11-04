from os import getenv, path
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    DB_URL: str = getenv("DB_URL")
    LOGGER_LEVEL: str = getenv("LOGGER_LEVEL", "INFO").upper()
    PROJECT_DIR: str = path.abspath(path.join(path.dirname(__file__), "../.."))
    LOG_DIR: str = path.join(PROJECT_DIR, "logs")
