import hashlib
import hmac
import secrets


ALGORITHM = "sha256"
ITERATIONS = 600_000
SALT_LENGTH = 16


def hash_password(password):
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    salt = secrets.token_bytes(SALT_LENGTH)

    password_hash = hashlib.pbkdf2_hmac(
        ALGORITHM,
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return (
        f"pbkdf2_{ALGORITHM}${ITERATIONS}$"
        f"{salt.hex()}${password_hash.hex()}"
    )


def verify_password(password, stored_hash):
    """
    Verify a password against a stored password hash.
    """
    if not isinstance(password, str):
        return False

    if not isinstance(stored_hash, str):
        return False

    try:
        algorithm_part, iterations, salt_hex, hash_hex = (
            stored_hash.split("$")
        )

        if not algorithm_part.startswith("pbkdf2_"):
            return False

        algorithm = algorithm_part.replace(
            "pbkdf2_",
            "",
            1,
        )

        iterations = int(iterations)

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            algorithm,
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash,
        )

    except (ValueError, TypeError):
        return False
