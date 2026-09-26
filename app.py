from core.utils import (
    clear_screen,
    print_banner,
    print_section,
    print_success,
    print_error,
    pause,
)

from core.logger import logger
from core.validators import validate_menu_choice
from core.error_handler import safe_run
from core.config import APP_VERSION
from core.commands import COMMANDS
from database.manager import (
    authenticate_user,
    initialize_database,
    set_metadata,
)
from core.session import Session

def login():
    """
    Authenticate a user before allowing access
    to the main toolkit menu.
    """
    print_section("User Login")

    username = input("Username: ").strip()

    if not username:
        print_error("Username cannot be empty.")
        return None

    password = input("Password: ")

    if not password:
        print_error("Password cannot be empty.")
        return None

    user = authenticate_user(
        username,
        password,
    )

    if user is None:
        print_error("Invalid username or password.")
        return None

    print_success(
        f"Welcome, {user['username']}!"
    )

    return user

def show_menu():
    print_section("MAIN MENU")

    for number, (name, _) in COMMANDS.items():
        print(f"[{number}] {name}")

    print("[0] Exit")


def main():
    initialize_database()
    set_metadata("app_version", APP_VERSION)
    user = login()

    if user is None:
        logger.warning("Login failed.")
        return
    session.login(user)

    logger.info(
        "User '%s' logged in successfully.",
        session.get_username(),
    )
    print_info(
        f"Logged in as: {session.get_username()}"
    )

    logger.info("Cyber Nexus Security Toolkit started")
    logger.info("Application version: %s", APP_VERSION)

    while True:
        clear_screen()
        print_banner()
        show_menu()

        choice = input("\nSelect an option: ").strip()

        logger.info("Menu option selected: %s", choice)

        if choice == "0":
            print("\nExiting Cyber Nexus Security Toolkit...")
            logger.info("Cyber Nexus Security Toolkit stopped")
            break

        if not validate_menu_choice(choice, 0, 10):
            print_error("Invalid option. Please select 0-10.")
            pause()
            continue

        command = COMMANDS.get(choice)

        if command is None:
            print_error("Command not found.")
            pause()
            continue

        name, function = command

        clear_screen()
        print_banner()

        safe_run(function, name)

        if choice != "8":
            pause()

if __name__ == "__main__":
    main()
