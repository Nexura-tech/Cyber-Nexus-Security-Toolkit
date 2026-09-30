from getpass import getpass

from core.commands import COMMANDS
from core.config import (
    APP_NAME,
    APP_VERSION,
    MAX_LOGIN_ATTEMPTS,
)
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
    create_first_admin,
    get_admin_count,
    get_user_count,
    initialize_database,
    set_metadata,
)


def show_menu(session):
    print_section("Main Menu")

    print("1. Password Analyzer")
    print("2. Hash Generator")
    print("3. System Information")
    print("4. URL Analyzer")
    print("5. Security Header Checker")
    print("6. File Metadata Analyzer")
    print("7. Log Analyzer")
    print("8. Reports Manager")
    print("9. Health Check")
    print("10. Settings")
    print("11. Security Dashboard")

    if session.is_admin():
        print("12. User Management")

    print("13. Logout")
    print("0. Exit")


def setup_first_admin():
    """
    Create the first administrator account.

    The administrator username is fixed by configuration.
    """

    from core.config import ADMIN_USERNAME

    print_section("First-Time Administrator Setup")

    print_info(
        f"Administrator username: {ADMIN_USERNAME}"
    )

    password = getpass(
        "Create administrator password: "
    )

    if not password:
        print_error(
            "Password cannot be empty."
        )
        return False

    confirm_password = getpass(
        "Confirm administrator password: "
    )

    if password != confirm_password:
        print_error(
            "Passwords do not match."
        )
        return False

    try:
        create_first_admin(
            ADMIN_USERNAME,
            password,
        )

        print_success(
            f"Administrator '{ADMIN_USERNAME}' "
            "created successfully."
        )

        pause()

        return True

    except ValueError as error:
        print_error(str(error))
        return False


def login(session=None):
    """
    Authenticate a user before allowing access
    to the main toolkit menu.

    The session parameter is optional so existing
    tests can continue to call login() directly.
    """

    if session is None:
        session = Session()

    print_section("User Login")

    username = input(
        "Username: "
    ).strip()

    if not username:
        print_error(
            "Username cannot be empty."
        )
        return None

    if (
        session.get_failed_login_attempts()
        >= MAX_LOGIN_ATTEMPTS
    ):
        print_error(
            "Too many failed login attempts."
        )

        print_warning(
            "Please restart the application "
            "before trying again."
        )

        return None

    password = getpass(
        "Password: "
    )

    if not password:
        print_error(
            "Password cannot be empty."
        )
        return None

    user = authenticate_user(
        username,
        password,
    )

    if user is None:

        session.record_failed_login()

        remaining = (
            MAX_LOGIN_ATTEMPTS
            - session.get_failed_login_attempts()
        )

        print_error(
            "Invalid username or password."
        )

        if remaining > 0:
            print_warning(
                f"Login attempts remaining: "
                f"{remaining}"
            )
        else:
            print_warning(
                "Maximum login attempts reached."
            )

        return None

    session.reset_failed_logins()

    print_success(
        f"Welcome, {user['username']}!"
    )

    logger.info(
        "User '%s' logged in with role '%s'.",
        user["username"],
        user["role"],
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


def run_command(choice, session):
    """
    Execute the selected toolkit command.
    """

    command = COMMANDS.get(choice)

    if command is None:
        print_error(
            "Invalid menu choice."
        )
        return

    # Security Dashboard and User Management
    # are available only to administrators.
    if (
        choice in ("11", "12")
        and not session.is_admin()
    ):
        print_error(
            "Access denied. "
            "Administrator privileges required."
        )

        logger.warning(
            "Unauthorized admin module access "
            "attempt by '%s'.",
            session.get_username(),
        )

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

        print_info(
            f"Role: {session.get_role()}"
        )

        show_menu(session)

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # Exit application
        if choice == "0":

            logger.info(
                "Application exited by user '%s'.",
                session.get_username(),
            )

            print_info(
                "Exiting Cyber Nexus Security Toolkit..."
            )

            return False

        # Logout
        if choice == "13":

            logout(session)

            pause()

            return True

        if not validate_menu_choice(
            choice,
            1,
            13,
        ):

            print_error(
                "Invalid choice. Please select 0-13."
            )

            pause()

            continue

        run_command(
            choice,
            session,
        )

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

        # First administrator setup.
        if get_admin_count() == 0:

            if get_user_count() == 0:

                if not setup_first_admin():
                    return

            else:

                print_warning(
                    "No administrator account exists."
                )

                print_info(
                    "Existing users were not modified."
                )

                print_info(
                    "Administrator setup requires "
                    "the configured administrator account."
                )

                pause()

        set_metadata(
            "app_version",
            APP_VERSION,
        )

        session = Session()

        while True:

            clear_screen()

            print_banner()

            if not session.is_authenticated():

                print_info(
                    "Please log in to continue."
                )

                user = login(session)

                if user is None:

                    pause()

                    continue

                session.login(user)

                logger.info(
                    "Session started for user '%s'.",
                    session.get_username(),
                )

            should_continue = main_menu(
                session
            )

            if should_continue is False:
                break

    except KeyboardInterrupt:

        print_warning(
            "\nApplication interrupted by user."
        )

        logger.info(
            "Application interrupted by user."
        )

    except Exception as error:

        print_error(
            "Application failed unexpectedly."
        )

        logger.exception(
            "Fatal application error: %s",
            error,
        )


if __name__ == "__main__":
    main()
