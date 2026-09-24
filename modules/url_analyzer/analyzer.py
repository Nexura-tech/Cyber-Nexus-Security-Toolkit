from urllib.parse import urlparse
import ipaddress


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
            "has_credentials": bool(parsed.username or parsed.password),
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

    print(
        f"IP Address Used: "
        f"{'YES' if result['is_ip'] else 'NO'}"
    )

    print(
        f"HTTPS: "
        f"{'YES' if result['https'] else 'NO'}"
    )

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

    if not result["is_ip"] and result["https"] and not result["has_credentials"]:
        print("[+] No basic URL concerns detected.")


def run():
    print("\nURL Analyzer")
    print("-" * 30)

    url = input("Enter URL: ")

    result = analyze_url(url)

    if result is None:
        print("\n[!] Invalid URL.")
        return

    display_result(result)


if __name__ == "__main__":
    run()
