import hashlib

from core.reporter import save_json, save_text


ALGORITHMS = {
    "1": "md5",
    "2": "sha1",
    "3": "sha256",
    "4": "sha512",
}


def generate_hash(text, algorithm):
    data = text.encode("utf-8")

    if algorithm == "md5":
        return hashlib.md5(data).hexdigest()

    if algorithm == "sha1":
        return hashlib.sha1(data).hexdigest()

    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()

    if algorithm == "sha512":
        return hashlib.sha512(data).hexdigest()

    return None


def get_algorithm_note(algorithm):
    if algorithm == "md5":
        return "Legacy checksum algorithm. Not recommended for security-sensitive use."

    if algorithm == "sha1":
        return "Legacy algorithm. Not recommended for security-sensitive use."

    return "Suitable modern cryptographic hash for general integrity/checksum use."


def run():
    print("\nHash Generator")
    print("-" * 30)

    text = input("Enter test text: ")

    print("\nAlgorithms:")
    print("1. MD5")
    print("2. SHA-1")
    print("3. SHA-256")
    print("4. SHA-512")

    choice = input("\nSelect algorithm: ").strip()

    algorithm = ALGORITHMS.get(choice)

    if algorithm is None:
        print("\n[!] Invalid selection.")
        return

    result = generate_hash(text, algorithm)
    note = get_algorithm_note(algorithm)

    print(f"\n{algorithm.upper()}:")
    print(result)

    print("\nInformation")
    print("-" * 30)
    print(note)

    report_data = {
        "module": "Hash Generator",
        "algorithm": algorithm.upper(),
        "hash": result,
        "note": note,
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "Hash Generator",
        "Algorithm": algorithm.upper(),
        "Hash": result,
        "Information": note,
    }

    text_file = save_text(
        "Cyber Nexus Hash Generation Report",
        text_data
    )

    print("\nReports Generated")
    print("-" * 40)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
