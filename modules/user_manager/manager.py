from database.manager import (
    create_user,
    get_all_users,
    set_user_active,
)
from core.utils import print_error, print_success, print_warning


def list_users():
    """
    Display all registered users.
    """
    users = get_all_users()

    if not users:
        print_warning("No users found.")
        return

    print("\nRegistered Users")
    print("=" * 60)

    for user in users:
        status = (
            "Active"
            if user["is_active"]
            else "Inactive"
        )

        print(
            f"ID: {user['id']} | "
            f"Username: {user['username']} | "
            f"Role: {user['role']} | "
            f"Status: {status} | "
            f"Created: {user['created_at']}"
        )


def add_user():
    """
    Create a new user.
    """
    print("\nCreate New User")
    print("=" * 60)

    username = input("Username: ").strip()

    if not username:
        print_error("Username cannot be empty.")
        return

    password = input("Password: ")

    if not password:
        print_error("Password cannot be empty.")
        return

    try:
        user_id = create_user(
            username,
            password,
        )

        print_success(
            f"User '{username}' created successfully. "
            f"User ID: {user_id}"
        )

    except ValueError as error:
        print_error(str(error))


def change_user_status():
    """
    Activate or deactivate a user.
    """
    username = input(
        "Enter username: "
    ).strip()

    if not username:
        print_error("Username cannot be empty.")
        return

    action = input(
        "Activate or deactivate? [a/d]: "
    ).strip().lower()

    if action not in ("a", "d"):
        print_error("Invalid option.")
        return

    is_active = action == "a"

    result = set_user_active(
        username,
        is_active,
    )

    if not result:
        print_error(
            f"User '{username}' was not found."
        )
        return

    status = "activated" if is_active else "deactivated"

    print_success(
        f"User '{username}' {status} successfully."
    )


def run():
    """
    User Management menu.
    """
    while True:
        print("\nUser Management")
        print("=" * 60)
        print("1. List Users")
        print("2. Create User")
        print("3. Activate/Deactivate User")
        print("0. Back")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            list_users()

        elif choice == "2":
            add_user()

        elif choice == "3":
            change_user_status()

        elif choice == "0":
            break

        else:
            print_error("Invalid choice.")
