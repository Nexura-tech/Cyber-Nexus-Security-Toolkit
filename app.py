from core.utils import (
    clear_screen,
    print_banner,
    print_section,
    print_error,
    pause,
)

from core.logger import logger
from modules.report_manager.manager import run as reports_manager
from modules.settings.manager import run as settings_manager
from core.validators import validate_menu_choice

from modules.password_analyzer.analyzer import (
    run as password_analyzer
)

from modules.hash_tool.hasher import (
    run as hash_generator
)

from modules.system_info.info import (
    run as system_information
)

from modules.url_analyzer.analyzer import (
    run as url_analyzer
)

from modules.security_headers.checker import (
    run as security_header_checker
)

from modules.metadata_analyzer.analyzer import (
    run as metadata_analyzer
)

from modules.log_analyzer.analyzer import (
    run as log_analyzer
)


def show_menu():
    print_section("MAIN MENU")

    print("[1] 🔐 Password Analyzer")
    print("[2] #️⃣  Hash Generator")
    print("[3] 🖥️  System Information")
    print("[4] 🌐 URL Analyzer")
    print("[5] 🛡️  Security Header Checker")
    print("[6] 📄 File Metadata Analyzer")
    print("[7] 📋 Log Analyzer")
    print("[8] 📊 Reports Manager")
    print("[9] ⚙️  Settings")
    print("[0] 🚪 Exit")


def main():
    logger.info("Cyber Nexus Security Toolkit started")

    while True:

        clear_screen()

        print_banner()
        show_menu()

        choice = input("\nSelect an option: ").strip()
        logger.info("Menu option selected: %s", choice)
        if not validate_menu_choice(choice, 0, 9):
            print_error("Invalid option. Please select 0-9.")
            pause()
            continue

        clear_screen()
        print_banner()

        if choice == "1":
            password_analyzer()
            pause()

        elif choice == "2":
            hash_generator()
            pause()

        elif choice == "3":
            system_information()
            pause()

        elif choice == "4":
            url_analyzer()
            pause()

        elif choice == "5":
            security_header_checker()
            pause()

        elif choice == "6":
            metadata_analyzer()
            pause()

        elif choice == "7":
            log_analyzer()
            pause()

        elif choice == "8":
            reports_manager()
        elif choice == "9":
            settings_manager()
            pause()
        elif choice == "0":
            logger.info("Cyber Nexus Security Toolkit stopped")
            print("\nExiting Cyber Nexus Security Toolkit...")
            break

        else:
            print_error("Invalid option. Please select 0-7.")
            pause()


if __name__ == "__main__":
    main()
