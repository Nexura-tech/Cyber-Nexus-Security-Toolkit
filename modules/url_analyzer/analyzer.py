from urllib.parse import urlparse
import ipaddress

from core.reporter import save_json, save_text


def normalize_url(url):
    url = url.strip()

    if not url:
        return None

    if "://" not in url:
        url = "https://" + url

    return url


def analyze_url(url):
    url = normalize_url(url)

    if url is None:
        return None

    try:
        parsed = urlparse(url)

        if not parsed.hostname:
            return None

        hostname = parsed.hostname

        try:
            ipaddress.ip_address(hostname)
            is_ip = True
        except ValueError:
            is_ip = False

        result = {
            "url": url,
            "scheme": parsed.scheme.lower(),
            "hostname": hostname,
            "port": parsed.port,
            "path": parsed.path,
            "query": parsed.query,
            "fragment": parsed.fragment,
            "has_credentials": bool(
                parsed.username or parsed.password
            ),
            "is_ip": is_ip,
            "https": parsed.scheme.lower() == "https",
            "length": len(url),
        }

        return result

    except ValueError:
        return None


def display_result(result):
    print("\nURL Analysis")
    print("-" * 40)

    print(f"URL: {result['url']}")
    print(f"Scheme: {result['scheme'].upper()}")
    print(f"Hostname: {result['hostname']}")

    if result["port"]:
        print(f"Port: {result['port']}")
    else:
        print("Port: Default")

    print(f"Path: {result['path'] or '/'}")
    print(f"IP Address Used: {'YES' if result['is_ip'] else 'NO'}")
    print(f"HTTPS: {'YES' if result['https'] else 'NO'}")
    print(
        f"Credentials in URL: "
        f"{'YES' if result['has_credentials'] else 'NO'}"
    )
    print(f"URL Length: {result['length']} characters")

    print("\nObservations")
    print("-" * 40)

    if result["is_ip"]:
        print("[!] Host is an IP address instead of a domain.")

    if not result["https"]:
        print("[!] URL is not using HTTPS.")

    if result["has_credentials"]:
        print("[!] URL contains embedded credentials.")

    if (
        not result["is_ip"]
        and result["https"]
        and not result["has_credentials"]
    ):
        print("[+] No basic URL concerns detected.")


def generate_reports(result):
    report_data = {
        "module": "URL Analyzer",
        "result": result,
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "URL Analyzer",
        "URL": result["url"],
        "Scheme": result["scheme"].upper(),
        "Hostname": result["hostname"],
        "Port": result["port"] or "Default",
        "Path": result["path"] or "/",
        "IP Address Used": result["is_ip"],
        "HTTPS": result["https"],
        "Credentials in URL": result["has_credentials"],
        "URL Length": result["length"],
    }

    text_file = save_text(
        "Cyber Nexus URL Analysis Report",
        text_data
    )

    return json_file, text_file


def run():
    print("\nURL Analyzer")
    print("-" * 30)

    url = input("Enter URL: ")

    result = analyze_url(url)

    if result is None:
        print("\n[!] Invalid URL.")
        return

    display_result(result)

    json_file, text_file = generate_reports(result)

    print("\nReports Generated")
    print("-" * 40)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
