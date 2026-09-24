import re
from pathlib import Path
from collections import Counter

from core.reporter import save_json, save_text


IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def analyze_log(file_path):
    path = Path(file_path)

    if not path.exists():
        print("\n[!] Log file does not exist.")
        return None

    if not path.is_file():
        print("\n[!] Provided path is not a file.")
        return None

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            lines = file.readlines()

    except OSError as error:
        print(f"\n[!] Could not read log file: {error}")
        return None

    total_lines = len(lines)

    failed_logins = 0
    successful_logins = 0

    ip_addresses = []

    for line in lines:
        lower_line = line.lower()

        if (
            "failed password" in lower_line
            or "failed login" in lower_line
            or "authentication failure" in lower_line
        ):
            failed_logins += 1

        if (
            "accepted password" in lower_line
            or "successful login" in lower_line
            or "login successful" in lower_line
        ):
            successful_logins += 1

        found_ips = IP_PATTERN.findall(line)
        ip_addresses.extend(found_ips)

    ip_counter = Counter(ip_addresses)

    return {
        "total_lines": total_lines,
        "failed_logins": failed_logins,
        "successful_logins": successful_logins,
        "ip_counter": dict(ip_counter),
    }


def display_results(results):
    print("\nLog Analysis")
    print("-" * 50)

    print(
        f"Total log entries: "
        f"{results['total_lines']}"
    )

    print(
        f"Failed login events: "
        f"{results['failed_logins']}"
    )

    print(
        f"Successful login events: "
        f"{results['successful_logins']}"
    )

    print("\nSource IP Summary")
    print("-" * 50)

    if not results["ip_counter"]:
        print("No IPv4 addresses found.")

    else:
        for ip, count in sorted(
            results["ip_counter"].items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(
                f"{ip:<18} "
                f"{count} occurrence(s)"
            )

    print("\nObservations")
    print("-" * 50)

    if results["failed_logins"] > 0:
        print(
            f"[!] {results['failed_logins']} "
            "failed authentication event(s) detected."
        )
    else:
        print(
            "[+] No failed authentication events detected."
        )

    if results["successful_logins"] > 0:
        print(
            f"[+] {results['successful_logins']} "
            "successful authentication event(s) detected."
        )


def generate_reports(results):
    report_data = {
        "module": "Log Analyzer",
        "summary": {
            "total_lines": results["total_lines"],
            "failed_logins": results["failed_logins"],
            "successful_logins": results["successful_logins"],
        },
        "source_ips": results["ip_counter"],
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "Log Analyzer",
        "Total Log Entries": results["total_lines"],
        "Failed Login Events": results["failed_logins"],
        "Successful Login Events": results["successful_logins"],
    }

    for ip, count in sorted(
        results["ip_counter"].items(),
        key=lambda item: item[1],
        reverse=True
    ):
        text_data[f"IP {ip}"] = (
            f"{count} occurrence(s)"
        )

    text_file = save_text(
        "Cyber Nexus Log Analysis Report",
        text_data
    )

    return json_file, text_file


def run():
    print("\nLog Analyzer")
    print("-" * 30)

    file_path = input(
        "Enter log file path: "
    ).strip()

    results = analyze_log(file_path)

    if results is None:
        return

    display_results(results)

    json_file, text_file = generate_reports(
        results
    )

    print("\nReports Generated")
    print("-" * 50)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
