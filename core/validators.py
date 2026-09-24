from pathlib import Path
from urllib.parse import urlparse


def validate_non_empty(value):
    """
    Check whether input contains meaningful text.
    """
    return bool(value and value.strip())


def validate_file_path(file_path):
    """
    Check whether a path exists and points to a regular file.
    """
    if not validate_non_empty(file_path):
        return False

    path = Path(file_path.strip())

    return path.exists() and path.is_file()


def validate_url(url):
    """
    Basic URL validation.
    """
    if not validate_non_empty(url):
        return False

    url = url.strip()

    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urlparse(url)

        return bool(
            parsed.scheme in ("http", "https")
            and parsed.hostname
        )

    except ValueError:
        return False


def validate_menu_choice(choice, minimum, maximum):
    """
    Validate a numeric menu choice.
    """
    if not choice or not choice.isdigit():
        return False

    value = int(choice)

    return minimum <= value <= maximum
