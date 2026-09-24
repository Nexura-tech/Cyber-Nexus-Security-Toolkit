from core.validators import (
    validate_non_empty,
    validate_file_path,
    validate_url,
    validate_menu_choice,
)


def test_validate_non_empty():
    assert validate_non_empty("hello") is True
    assert validate_non_empty("   ") is False
    assert validate_non_empty("") is False
    assert validate_non_empty(None) is False


def test_validate_file_path():
    assert validate_file_path("app.py") is True
    assert validate_file_path("does_not_exist.txt") is False
    assert validate_file_path("") is False
    assert validate_file_path(None) is False


def test_validate_url():
    assert validate_url("https://example.com") is True
    assert validate_url("http://example.com") is True
    assert validate_url("example.com") is True
    assert validate_url("") is False
    assert validate_url(None) is False


def test_validate_menu_choice():
    assert validate_menu_choice("0", 0, 10) is True
    assert validate_menu_choice("5", 0, 10) is True
    assert validate_menu_choice("10", 0, 10) is True

    assert validate_menu_choice("11", 0, 10) is False
    assert validate_menu_choice("-1", 0, 10) is False
    assert validate_menu_choice("abc", 0, 10) is False
    assert validate_menu_choice("", 0, 10) is False
    assert validate_menu_choice(None, 0, 10) is False


def test_menu_choice_with_spaces():
    assert validate_menu_choice(" 5 ", 0, 10) is True
