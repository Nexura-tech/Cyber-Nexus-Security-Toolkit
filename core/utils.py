from datetime import datetime


def print_banner():
    print("=" * 60)
    print("        CYBER NEXUS SECURITY TOOLKIT")
    print("        Defensive Security Toolkit")
    print("=" * 60)


def print_section(title):
    print()
    print("-" * 60)
    print(title)
    print("-" * 60)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pause():
    input("\nPress Enter to continue...")
