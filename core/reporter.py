import json
import re
from datetime import datetime

from core.config import REPORT_DIR


def sanitize_name(name):
    """
    Convert a module/report name into a safe filename component.
    """
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def generate_filename(extension, prefix="security_report"):
    """
    Generate a unique report filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_prefix = sanitize_name(prefix)

    return REPORT_DIR / f"{safe_prefix}_{timestamp}.{extension}"


def save_json(data, prefix=None):
    """
    Save report data as JSON.
    """
    if prefix is None:
        prefix = data.get("module", "security_report")

    file_path = generate_filename("json", prefix)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, default=str)

    return file_path


def save_text(title, data, prefix=None):
    """
    Save report data as readable text.
    """
    if prefix is None:
        prefix = title

    file_path = generate_filename("txt", prefix)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{title}\n")
        file.write("=" * 60 + "\n\n")

        if isinstance(data, dict):
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
        else:
            file.write(str(data))

    return file_path
