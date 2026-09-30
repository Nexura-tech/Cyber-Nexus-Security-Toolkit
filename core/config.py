from dotenv import load_dotenv
import os
from pathlib import Path
ADMIN_USERNAME = "Sabbo"

APP_NAME = "Cyber Nexus Security Toolkit"
BASE_DIR = Path(__file__).resolve().parent.parent
if os.getenv("PYTEST_CURRENT_TEST") is None:
    load_dotenv(BASE_DIR / ".env")
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "toolkit.log"


def get_int_env(name, default, minimum=None):
    """
    Read an integer environment variable safely.
    Falls back to default if the value is invalid.
    """
    value = os.getenv(name)

    if value is None:
        return default

    try:
        value = int(value)
    except ValueError:
        return default

    if minimum is not None and value < minimum:
        return default

    return value


APP_VERSION = os.getenv(
    "CYBER_NEXUS_APP_VERSION",
    "1.0.0",
)

REQUEST_TIMEOUT = get_int_env(
    "CYBER_NEXUS_REQUEST_TIMEOUT",
    10,
    minimum=1,
)


REPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

MAX_LOGIN_ATTEMPTS = get_int_env(
    "CYBER_NEXUS_MAX_LOGIN_ATTEMPTS",
    5,
    minimum=1,
)

LOGIN_LOCKOUT_SECONDS = get_int_env(
    "CYBER_NEXUS_LOGIN_LOCKOUT_SECONDS",
    60,
    minimum=1,
)
