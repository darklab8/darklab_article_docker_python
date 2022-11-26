from utils.config_parser import ConfigParser
from utils.logger import Logger

logger = Logger(console_level="DEBUG", name=__name__)
config = ConfigParser(settings_prefix="example")

DATABASE_USER = config.get("database_username", "postgres")
DATABASE_PASSWORD = config.get("database_password", "postgres")
DATABASE_HOST = config.get("database_host", "db")
DATABASE_URL = config.get(
    "database_url", f"{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/"
)

DATABASE_NAME = "default"
DATABASE_DEBUG = bool(config.get("database_debug", ""))

CELERY_BROKER = config.get("celery.broker", "")
CELERY_BACKEND = config.get("celery.backend", "")

LOGGER_CONSOLE_LEVEL = config.get("logger.console.level", "INFO")