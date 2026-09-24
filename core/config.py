import os
from pathlib import Path


APP_NAME = "Cyber Nexus Security Toolkit"

APP_VERSION = os.getenv(
    "CYBER_NEXUS_APP_VERSION",
    "1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "toolkit.log"

REQUEST_TIMEOUT = int(
    os.getenv(
        "CYBER_NEXUS_REQUEST_TIMEOUT",
        "10",
    )
)

REPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
