from modules.hash_tool.hasher import generate_hash


def test_md5_hash():
    result = generate_hash("hello", "md5")

    assert result == "5d41402abc4b2a76b9719d911017c592"


def test_sha256_hash():
    result = generate_hash("hello", "sha256")

    assert result == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_sha512_hash():
    result = generate_hash("hello", "sha512")

    assert len(result) == 128


def test_invalid_algorithm():
    result = generate_hash("hello", "invalid")

    assert result is None
