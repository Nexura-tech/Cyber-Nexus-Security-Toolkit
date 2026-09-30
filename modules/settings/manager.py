import os
from platform import python_version
from core.logger import logger
from core.config import (
    APP_NAME,
    APP_VERSION,
    BASE_DIR,
    REPORT_DIR,
    LOG_DIR,
    LOG_FILE,
    REQUEST_TIMEOUT,
)


ENV_FILE = BASE_DIR / ".env"


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


def save_request_timeout(value):
    """Save request timeout to the local .env file."""

    lines = []

    if ENV_FILE.exists():
        lines = ENV_FILE.read_text(
            encoding="utf-8"
        ).splitlines()

    updated = False
    new_lines = []

    for line in lines:
        if line.startswith("CYBER_NEXUS_REQUEST_TIMEOUT="):
            new_lines.append(
                f"CYBER_NEXUS_REQUEST_TIMEOUT={value}"
            )
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(
            f"CYBER_NEXUS_REQUEST_TIMEOUT={value}"
        )

    ENV_FILE.write_text(
        "\n".join(new_lines) + "\n",
        encoding="utf-8",
    )


def change_request_timeout():
    print("\nChange Request Timeout")
    print("-" * 60)

    print(f"Current Timeout: {REQUEST_TIMEOUT} seconds")

    value = input(
        "Enter new timeout in seconds: "
    ).strip()

    if not value.isdigit():
        print("\n[!] Timeout must be a positive integer.")
        return

    timeout = int(value)

    if timeout < 1:
        print("\n[!] Timeout must be at least 1 second.")
        return

    if timeout > 300:
        print("\n[!] Timeout cannot exceed 300 seconds.")
        return

    try:
        save_request_timeout(timeout)
        logger.info(
            "Request timeout changed from %s to %s seconds.",
            REQUEST_TIMEOUT,
            timeout,
        )
        print(
            f"\n[+] Request timeout saved: "
            f"{timeout} seconds"
        )
        print(
            "[i] Restart the application for the "
            "new value to take effect."
        )
    except OSError as error:
        print(f"\n[!] Could not save setting: {error}")


def run():
    while True:
        print("\nSettings")
        print("-" * 60)
        print("[1] View Application Settings")
        print("[2] Change Request Timeout")
        print("[0] Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            show_settings()

        elif choice == "2":
            change_request_timeout()

        elif choice == "0":
            break

        else:
            print("\n[!] Invalid option.")

        if choice != "0":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    run()
