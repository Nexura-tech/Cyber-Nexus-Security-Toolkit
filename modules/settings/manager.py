from platform import python_version

from core.config import (
    APP_NAME,
    APP_VERSION,
    BASE_DIR,
    REPORT_DIR,
    LOG_DIR,
    LOG_FILE,
    REQUEST_TIMEOUT,
)


def show_settings():
    print("\nApplication Settings")
    print("-" * 60)

    print(f"Application Name : {APP_NAME}")
    print(f"Version          : {APP_VERSION}")
    print(f"Python Version   : {python_version()}")
    print(f"Project Directory: {BASE_DIR}")
    print(f"Reports Directory: {REPORT_DIR}")
    print(f"Logs Directory   : {LOG_DIR}")
    print(f"Log File         : {LOG_FILE}")
    print(f"Request Timeout  : {REQUEST_TIMEOUT} seconds")


def run():
    show_settings()


if __name__ == "__main__":
    run()
