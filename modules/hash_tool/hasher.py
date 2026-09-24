import hashlib


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


def run():
    print("\nHash Generator")
    print("-" * 30)

    text = input("Enter text: ")

    print("\nAlgorithms:")
    print("1. MD5")
    print("2. SHA-1")
    print("3. SHA-256")
    print("4. SHA-512")

    choice = input("\nSelect algorithm: ")

    algorithms = {
        "1": "md5",
        "2": "sha1",
        "3": "sha256",
        "4": "sha512",
    }

    algorithm = algorithms.get(choice)

    if algorithm is None:
        print("Invalid selection.")
        return

    result = generate_hash(text, algorithm)

    print(f"\n{algorithm.upper()}:")
    print(result)


if __name__ == "__main__":
    run()
