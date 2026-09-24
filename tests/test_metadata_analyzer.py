from modules.metadata_analyzer.analyzer import get_file_metadata


def test_metadata_for_existing_file():
    result = get_file_metadata("app.py")

    assert result is not None
    assert result["name"] == "app.py"
    assert result["extension"] == ".py"
    assert result["sha256"]


def test_metadata_for_missing_file():
    result = get_file_metadata("this_file_does_not_exist.txt")

    assert result is None
