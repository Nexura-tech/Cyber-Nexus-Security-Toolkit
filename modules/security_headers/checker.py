import requests


SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "description": "Forces browsers to use HTTPS.",
        "recommendation": "Enable HSTS on HTTPS websites."
    },
    "Content-Security-Policy": {
        "description": "Helps control which resources a browser can load.",
        "recommendation": "Define an appropriate Content-Security-Policy."
    },
    "X-Content-Type-Options": {
        "description": "Helps prevent MIME-type sniffing.",
        "recommendation": "Set X-Content-Type-Options to nosniff."
    },
    "X-Frame-Options": {
        "description": "Controls whether the page can be embedded in frames.",
        "recommendation": "Configure an appropriate X-Frame-Options policy."
    },
    "Referrer-Policy": {
        "description": "Controls referrer information sent with requests.",
        "recommendation": "Configure an appropriate Referrer-Policy."
    },
    "Permissions-Policy": {
        "description": "Controls access to selected browser features.",
        "recommendation": "Configure Permissions-Policy according to application requirements."
    }
}


def normalize_url(url):
    url = url.strip()

    if not url:
        return None

    if "://" not in url:
        url = "https://" + url

    return url


def check_headers(url):
    url = normalize_url(url)

    if url is None:
        return None

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        return response

    except requests.RequestException as error:
        print(f"\n[!] Request failed: {error}")
        return None


def display_results(response):
    print("\nSecurity Header Analysis")
    print("-" * 50)

    print(f"Final URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(f"Server: {response.headers.get('Server', 'Not disclosed')}")

    print("\nSecurity Headers")
    print("-" * 50)

    present = 0
    missing = 0

    for header, information in SECURITY_HEADERS.items():

        value = response.headers.get(header)

        if value:
            present += 1

            print(f"\n[+] {header}")
            print(f"    Status: PRESENT")
            print(f"    Value: {value}")

        else:
            missing += 1

            print(f"\n[-] {header}")
            print(f"    Status: MISSING")
            print(f"    Recommendation: {information['recommendation']}")

    print("\nSummary")
    print("-" * 50)

    print(f"Security headers present: {present}")
    print(f"Security headers missing: {missing}")


def run():
    print("\nSecurity Header Checker")
    print("-" * 30)

    url = input("Enter website URL: ")

    response = check_headers(url)

    if response is None:
        return

    display_results(response)


if __name__ == "__main__":
    run()
