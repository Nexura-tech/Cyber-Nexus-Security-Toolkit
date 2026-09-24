import hashlib
from pathlib import Path
from datetime import datetime

from core.reporter import save_json, save_text


def format_size(size):
    if size < 1024:
        return f"{size} B"

    if size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"

    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"

    return f"{size / (1024 ** 3):.2f} GB"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except OSError as error:
        return f"Error: {error}"


def get_file_metadata(file_path):
    path = Path(file_path)

    if not path.exists():
        return None

    if not path.is_file():
        return None

    stats = path.stat()

    metadata = {
        "name": path.name,
        "extension": path.suffix or "None",
        "type": (
            path.suffix[1:].upper()
            if path.suffix
            else "Unknown"
        ),
        "absolute_path": str(path.resolve()),
        "size": format_size(stats.st_size),
        "created": datetime.fromtimestamp(
            stats.st_ctime
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(
            stats.st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "accessed": datetime.fromtimestamp(
            stats.st_atime
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "sha256": calculate_sha256(path),
    }

    return metadata


def display_metadata(metadata):
    print("\nFile Metadata")
    print("-" * 50)

    print(f"Name:          {metadata['name']}")
    print(f"Extension:     {metadata['extension']}")
    print(f"Type:          {metadata['type']}")
    print(f"Path:          {metadata['absolute_path']}")
    print(f"Size:          {metadata['size']}")
    print(f"Created:       {metadata['created']}")
    print(f"Modified:      {metadata['modified']}")
    print(f"Accessed:      {metadata['accessed']}")

    print("\nSHA-256")
    print("-" * 50)
    print(metadata["sha256"])


def generate_reports(metadata):
    report_data = {
        "module": "File Metadata Analyzer",
        "result": metadata,
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "File Metadata Analyzer",
        "Name": metadata["name"],
        "Extension": metadata["extension"],
        "Type": metadata["type"],
        "Path": metadata["absolute_path"],
        "Size": metadata["size"],
        "Created": metadata["created"],
        "Modified": metadata["modified"],
        "Accessed": metadata["accessed"],
        "SHA-256": metadata["sha256"],
    }

    text_file = save_text(
        "Cyber Nexus File Metadata Report",
        text_data
    )

    return json_file, text_file


def run():
    print("\nFile Metadata Analyzer")
    print("-" * 30)

    file_path = input("Enter file path: ").strip()

    metadata = get_file_metadata(file_path)

    if metadata is None:
        print(
            "\n[!] File does not exist "
            "or is not a regular file."
        )
        return

    display_metadata(metadata)

    json_file, text_file = generate_reports(metadata)

    print("\nReports Generated")
    print("-" * 50)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
