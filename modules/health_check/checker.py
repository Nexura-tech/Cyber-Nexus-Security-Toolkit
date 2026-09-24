import importlib
from pathlib import Path

from core.config import REPORT_DIR, LOG_DIR
from core.utils import print_success, print_error, print_warning


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
    if directory.exists() and directory.is_dir():
        print_success(f"{name:<25} OK")
        return True

    print_error(f"{name:<25} FAILED")
    return False


def check_dependency(module_name, display_name):
    try:
        importlib.import_module(module_name)
        print_success(f"{display_name:<25} OK")
        return True
    except ImportError:
        print_error(f"{display_name:<25} FAILED")
        return False


def check_modules():
    status = True

    for name, module in MODULES.items():
        try:
            importlib.import_module(module)
            print_success(f"{name:<25} OK")
        except Exception as error:
            print_error(f"{name:<25} FAILED")
            print_warning(f"  Reason: {error}")
            status = False

    return status


def run():
    print("\nCyber Nexus Health Check")
    print("=" * 60)

    total_checks = 0
    passed_checks = 0

    print("\nDirectories")
    print("-" * 60)

    for directory, name in [
        (REPORT_DIR, "Reports Directory"),
        (LOG_DIR, "Logs Directory"),
    ]:
        total_checks += 1

        if check_directory(directory, name):
            passed_checks += 1

    print("\nDependencies")
    print("-" * 60)

    for module_name, display_name in [
        ("requests", "Requests Library"),
        ("colorama", "Colorama Library"),
    ]:
        total_checks += 1

        if check_dependency(module_name, display_name):
            passed_checks += 1

    print("\nApplication Modules")
    print("-" * 60)

    for name, module in MODULES.items():
        total_checks += 1

        try:
            importlib.import_module(module)
            print_success(f"{name:<25} OK")
            passed_checks += 1
        except Exception as error:
            print_error(f"{name:<25} FAILED")
            print_warning(f"  Reason: {error}")

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
