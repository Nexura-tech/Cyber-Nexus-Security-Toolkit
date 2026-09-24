import requests
from core.config import REQUEST_TIMEOUT
from core.reporter import save_json, save_text


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
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        return response

    except requests.RequestException as error:
        print(f"\n[!] Request failed: {error}")
        return None


def analyze_headers(response):
    headers = {}

    for header, information in SECURITY_HEADERS.items():
        value = response.headers.get(header)

        headers[header] = {
            "present": bool(value),
            "value": value if value else None,
            "description": information["description"],
            "recommendation": (
                None
                if value
                else information["recommendation"]
            )
        }

    return headers


def display_results(response, headers):
    print("\nSecurity Header Analysis")
    print("-" * 50)

    print(f"Final URL: {response.url}")
    print(f"Status Code: {response.status_code}")
    print(
        f"Server: "
        f"{response.headers.get('Server', 'Not disclosed')}"
    )

    print("\nSecurity Headers")
    print("-" * 50)

    present = 0
    missing = 0

    for header, information in headers.items():

        if information["present"]:
            present += 1

            print(f"\n[+] {header}")
            print("    Status: PRESENT")
            print(f"    Value: {information['value']}")

        else:
            missing += 1

            print(f"\n[-] {header}")
            print("    Status: MISSING")
            print(
                f"    Recommendation: "
                f"{information['recommendation']}"
            )

    print("\nSummary")
    print("-" * 50)
    print(f"Security headers present: {present}")
    print(f"Security headers missing: {missing}")


def generate_reports(response, headers):
    present = sum(
        1
        for information in headers.values()
        if information["present"]
    )

    missing = len(headers) - present

    report_data = {
        "module": "Security Header Checker",
        "final_url": response.url,
        "status_code": response.status_code,
        "server": response.headers.get(
            "Server",
            "Not disclosed"
        ),
        "headers": headers,
        "summary": {
            "present": present,
            "missing": missing
        }
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "Security Header Checker",
        "Final URL": response.url,
        "Status Code": response.status_code,
        "Server": response.headers.get(
            "Server",
            "Not disclosed"
        ),
        "Headers Present": present,
        "Headers Missing": missing,
    }

    for header, information in headers.items():
        text_data[f"{header} - Status"] = (
            "PRESENT"
            if information["present"]
            else "MISSING"
        )

        if information["present"]:
            text_data[f"{header} - Value"] = information["value"]
        else:
            text_data[f"{header} - Recommendation"] = (
                information["recommendation"]
            )

    text_file = save_text(
        "Cyber Nexus Security Header Report",
        text_data
    )

    return json_file, text_file


def run():
    print("\nSecurity Header Checker")
    print("-" * 30)

    url = input("Enter website URL: ")

    response = check_headers(url)

    if response is None:
        return

    headers = analyze_headers(response)

    display_results(response, headers)

    json_file, text_file = generate_reports(
        response,
        headers
    )

    print("\nReports Generated")
    print("-" * 50)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
