import json
from datetime import datetime

from core.config import REPORT_DIR

def generate_filename(extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return REPORT_DIR / f"security_report_{timestamp}.{extension}"


def save_json(data):
    file_path = generate_filename("json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, default=str)

    return file_path


def save_text(title, data):
    file_path = generate_filename("txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{title}\n")
        file.write("=" * 60 + "\n\n")

        if isinstance(data, dict):
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
        else:
            file.write(str(data))

    return file_path
