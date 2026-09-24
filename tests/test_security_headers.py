from modules.security_headers.checker import analyze_headers


class FakeResponse:
    def __init__(self):
        self.headers = {
            "Strict-Transport-Security": "max-age=31536000",
            "Content-Security-Policy": "default-src 'self'",
            "X-Content-Type-Options": "nosniff",
        }


def test_security_headers_analysis():
    response = FakeResponse()

    result = analyze_headers(response)

    assert result["Strict-Transport-Security"]["present"] is True
    assert result["Content-Security-Policy"]["present"] is True
    assert result["X-Content-Type-Options"]["present"] is True


def test_missing_security_headers():
    response = FakeResponse()

    result = analyze_headers(response)

    assert result["X-Frame-Options"]["present"] is False
    assert result["Referrer-Policy"]["present"] is False
    assert result["Permissions-Policy"]["present"] is False
