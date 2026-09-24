from modules.url_analyzer.analyzer import analyze_url


def test_https_url():
    result = analyze_url("https://example.com")

    assert result is not None
    assert result["scheme"] == "https"
    assert result["hostname"] == "example.com"
    assert result["https"] is True


def test_url_without_scheme():
    result = analyze_url("example.com")

    assert result is not None
    assert result["scheme"] == "https"


def test_ip_url():
    result = analyze_url("http://192.168.1.1")

    assert result is not None
    assert result["is_ip"] is True

def test_invalid_url():
    result = analyze_url("")

    assert result is None
