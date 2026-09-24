import hashlib
from pathlib import Path
from datetime import datetime


def format_size(size):
    """Convert bytes into a human-readable format."""

    if size < 1024:
        return f"{size} B"

    if size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"

    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"

    return f"{size / (1024 ** 3):.2f} GB"


def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file."""

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
    """Collect basic file metadata."""

    path = Path(file_path)

    if not path.exists():
        return None

    if not path.is_file():
        return None

    stats = path.stat()

    metadata = {
        "name": path.name,
        "extension": path.suffix or "None",
        "type": path.suffix[1:].upper() if path.suffix else "Unknown",
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
    """Display file metadata."""

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


def run():
    print("\nFile Metadata Analyzer")
    print("-" * 30)

    file_path = input("Enter file path: ").strip()

    metadata = get_file_metadata(file_path)

    if metadata is None:
        print("\n[!] File does not exist or is not a regular file.")
        return

    display_metadata(metadata)


if __name__ == "__main__":
    run()
