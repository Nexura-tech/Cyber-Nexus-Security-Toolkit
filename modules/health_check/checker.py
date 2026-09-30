import importlib

from core.config import REPORT_DIR, LOG_DIR
from core.utils import (
    print_success,
    print_error,
    print_warning,
)


MODULES = {
    "Password Analyzer": "modules.password_analyzer.analyzer",
    "Hash Generator": "modules.hash_tool.hasher",
    "System Information": "modules.system_info.info",
    "URL Analyzer": "modules.url_analyzer.analyzer",
    "Security Header Checker": "modules.security_headers.checker",
    "Metadata Analyzer": "modules.metadata_analyzer.analyzer",
    "Log Analyzer": "modules.log_analyzer.analyzer",
    "Reports Manager": "modules.report_manager.manager",
    "Settings Manager": "modules.settings.manager",
}


def check_directory(directory, name):
    """Check whether a required directory exists."""

    if directory.exists() and directory.is_dir():
        print_success(f"{name:<25} OK")
        return True

    print_error(f"{name:<25} FAILED")
    return False


def check_dependency(module_name, display_name):
    """Check whether a required Python dependency can be imported."""

    try:
        importlib.import_module(module_name)
        print_success(f"{display_name:<25} OK")
        return True

    except ImportError as error:
        print_error(f"{display_name:<25} FAILED")
        print_warning(f"  Reason: {error}")
        return False


def check_application_module(module_name, display_name):
    """Check whether an application module can be imported."""

    try:
        importlib.import_module(module_name)
        print_success(f"{display_name:<25} OK")
        return True

    except Exception as error:
        print_error(f"{display_name:<25} FAILED")
        print_warning(f"  Reason: {error}")
        return False


def get_health_summary():
    """
    Run all health checks and return a summary.

    This function does not print the complete health-check report.
    It is designed to be reused by the dashboard and other components.
    """

    total_checks = 0
    passed_checks = 0

    directories = [
        (REPORT_DIR, "Reports Directory"),
        (LOG_DIR, "Logs Directory"),
    ]

    for directory, name in directories:
        total_checks += 1

        if directory.exists() and directory.is_dir():
            passed_checks += 1

    dependencies = [
        "requests",
        "colorama",
        "pytest",
    ]

    for module_name in dependencies:
        total_checks += 1

        try:
            importlib.import_module(module_name)
            passed_checks += 1
        except ImportError:
            pass

    for module_name in MODULES.values():
        total_checks += 1

        try:
            importlib.import_module(module_name)
            passed_checks += 1
        except Exception:
            pass

    failed_checks = total_checks - passed_checks

    if failed_checks == 0:
        status = "READY"
    else:
        status = "ATTENTION REQUIRED"

    return {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "status": status,
    }


def run():
    """Run the complete Cyber Nexus Health Check."""

    print("\nCyber Nexus Health Check")
    print("=" * 60)

    total_checks = 0
    passed_checks = 0

    print("\nDirectories")
    print("-" * 60)

    directories = [
        (REPORT_DIR, "Reports Directory"),
        (LOG_DIR, "Logs Directory"),
    ]

    for directory, name in directories:
        total_checks += 1

        if check_directory(directory, name):
            passed_checks += 1

    print("\nDependencies")
    print("-" * 60)

    dependencies = [
        ("requests", "Requests Library"),
        ("colorama", "Colorama Library"),
        ("pytest", "Pytest Library"),
    ]

    for module_name, display_name in dependencies:
        total_checks += 1

        if check_dependency(module_name, display_name):
            passed_checks += 1

    print("\nApplication Modules")
    print("-" * 60)

    for name, module in MODULES.items():
        total_checks += 1

        if check_application_module(module, name):
            passed_checks += 1

    failed_checks = total_checks - passed_checks

    print("\nHealth Summary")
    print("=" * 60)
    print(f"Total Checks : {total_checks}")
    print(f"Passed       : {passed_checks}")
    print(f"Failed       : {failed_checks}")

    if failed_checks == 0:
        print_success("Overall Status: READY")
    else:
        print_warning("Overall Status: ATTENTION REQUIRED")


if __name__ == "__main__":
    run()
