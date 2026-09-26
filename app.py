from core.commands import COMMANDS
from core.config import APP_NAME, APP_VERSION
from core.logger import logger
from core.session import Session
from core.utils import (
    clear_screen,
    pause,
    print_banner,
    print_error,
    print_info,
    print_section,
    print_success,
    print_warning,
)
from core.validators import validate_menu_choice

from database.manager import (
    authenticate_user,
    initialize_database,
    set_metadata,
)


def show_menu():
    """
    Display the main toolkit menu.
    """
    print_section("Main Menu")

    for number, (name, _) in COMMANDS.items():
        print(f"{number}. {name}")

    print("11. Logout")
    print("0. Exit")


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


def logout(session):
    """
    Log out the current user and clear the session.
    """
    username = session.get_username()

    if not session.is_authenticated():
        print_warning(
            "No user is currently logged in."
        )
        return False

    session.logout()

    print_success(
        f"User '{username}' logged out successfully."
    )

    logger.info(
        "User '%s' logged out.",
        username,
    )

    return True


def run_command(choice):
    """
    Execute the selected toolkit command.
    """
    command = COMMANDS.get(choice)

    if command is None:
        print_error("Invalid menu choice.")
        return

    command_name, command_function = command

    logger.info(
        "Starting module: %s",
        command_name,
    )

    try:
        command_function()

        logger.info(
            "Module completed: %s",
            command_name,
        )

    except KeyboardInterrupt:
        print_warning(
            f"{command_name} cancelled by user."
        )

        logger.info(
            "Module cancelled: %s",
            command_name,
        )

    except Exception as error:
        print_error(
            f"{command_name} failed."
        )

        logger.exception(
            "Module error in %s: %s",
            command_name,
            error,
        )


def main_menu(session):
    """
    Run the main authenticated toolkit menu.

    Returns:
        True  -> user logged out
        False -> user selected exit
    """
    while session.is_authenticated():

        clear_screen()
        print_banner()

        print_info(
            f"Logged in as: {session.get_username()}"
        )

        show_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "0":
            logger.info(
                "Application exited by user '%s'.",
                session.get_username(),
            )

            print_info(
                "Exiting Cyber Nexus Security Toolkit..."
            )

            return False

        if choice == "11":
            logout(session)
            pause()

            return True

        if not validate_menu_choice(
            choice,
            1,
            10,
        ):
            print_error(
                "Invalid choice. Please select 0-11."
            )
            pause()
            continue

        run_command(choice)
        pause()

    return True


def main():
    """
    Application entry point.
    """
    try:
        clear_screen()
        print_banner()

        print_info(
            f"Starting {APP_NAME} v{APP_VERSION}"
        )

        initialize_database()

        set_metadata(
            "app_version",
            APP_VERSION,
        )

        session = Session()

        while True:

            clear_screen()
            print_banner()

            user = login()

            if user is None:
                logger.warning(
                    "Login failed."
                )

                print_error(
                    "Authentication failed."
                )

                retry = input(
                    "\nTry again? [Y/n]: "
                ).strip().lower()

                if retry in ("n", "no"):
                    print_info(
                        "Goodbye!"
                    )

                    return

                continue

            session.login(user)

            logger.info(
                "User '%s' logged in successfully.",
                session.get_username(),
            )

            print_info(
                f"Logged in as: "
                f"{session.get_username()}"
            )

            pause()

            logged_out = main_menu(session)

            if not logged_out:
                break

            # User logged out.
            # Return to login screen.
            session.logout()

            print_info(
                "Returning to login screen..."
            )

            pause()

        logger.info(
            "Cyber Nexus Security Toolkit stopped."
        )

        clear_screen()
        print_banner()

        print_success(
            "Thank you for using Cyber Nexus Security Toolkit."
        )

    except KeyboardInterrupt:
        print()
        print_warning(
            "Application interrupted by user."
        )

        logger.info(
            "Application interrupted by user."
        )

    except Exception as error:
        print_error(
            "Application encountered an unexpected error."
        )

        logger.exception(
            "Fatal application error: %s",
            error,
        )


if __name__ == "__main__":
    main()
