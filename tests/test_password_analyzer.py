from modules.password_analyzer.analyzer import analyze_password


def test_weak_password():
    result = analyze_password("abc")
    assert result["strength"] == "Weak"


def test_strong_password():
    result = analyze_password("TestPassword123!")
    assert result["strength"] == "Strong"


def test_password_length():
    result = analyze_password("abcdef")
    assert result["length"] == 6


def test_password_character_checks():
    result = analyze_password("Test123!")
    assert result["uppercase"] is True
    assert result["lowercase"] is True
    assert result["digits"] is True
    assert result["special"] is True
