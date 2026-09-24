import os
from datetime import datetime

from colorama import Fore, Style, init


init(autoreset=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(Fore.CYAN + "=" * 60)
    print(
        Fore.CYAN
        + "        CYBER NEXUS SECURITY TOOLKIT"
    )
    print(
        Fore.WHITE
        + "        Defensive Security Toolkit"
    )
    print(Fore.CYAN + "=" * 60)


def print_section(title):
    print()
    print(Fore.BLUE + "-" * 60)
    print(Fore.BLUE + title)
    print(Fore.BLUE + "-" * 60)


def print_success(message):
    print(Fore.GREEN + f"[+] {message}")


def print_warning(message):
    print(Fore.YELLOW + f"[!] {message}")


def print_error(message):
    print(Fore.RED + f"[-] {message}")


def print_info(message):
    print(Fore.CYAN + f"[*] {message}")


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pause():
    input(
        Fore.WHITE
        + "\nPress Enter to continue..."
    )
