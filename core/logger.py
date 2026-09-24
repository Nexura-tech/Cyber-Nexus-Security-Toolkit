import logging

from core.config import LOG_DIR, LOG_FILE


LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("cyber_nexus")
