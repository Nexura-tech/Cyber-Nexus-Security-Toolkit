from pathlib import Path
from urllib.parse import urlparse


def validate_non_empty(value):
    """
    Check whether a value contains non-whitespace characters.
    """
    if value is None:
        return False

    return bool(str(value).strip())


def validate_file_path(file_path):
    """
    Check whether the supplied path exists and is a file.
    """
    if not validate_non_empty(file_path):
        return False

    path = Path(str(file_path).strip())

    return path.exists() and path.is_file()


def validate_url(url):
    """
    Validate a basic HTTP/HTTPS URL.
    """
    if not validate_non_empty(url):
        return False

    url = str(url).strip()

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
    Validate that a menu choice is an integer
    within the supplied range.
    """
    if choice is None:
        return False

    choice = str(choice).strip()

    if not choice.isdigit():
        return False

    value = int(choice)

    return minimum <= value <= maximum
