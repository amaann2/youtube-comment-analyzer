from app.core.config import Settings
from app.utils.logger_util import setup_logging

settings = Settings()

logger = setup_logging(settings)