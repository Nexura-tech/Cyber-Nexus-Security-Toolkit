from pathlib import Path

from core.reporter import REPORT_DIR


def list_reports():
    reports = sorted(
        REPORT_DIR.glob("*"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    reports = [
        report
        for report in reports
        if report.is_file()
    ]

    if not reports:
        print("\n[!] No reports found.")
        return

    print("\nAvailable Reports")
    print("-" * 70)

    for index, report in enumerate(reports, start=1):
        size = report.stat().st_size

        print(
            f"[{index}] "
            f"{report.name:<45} "
            f"{size} bytes"
        )


def view_latest_report():
    reports = sorted(
        REPORT_DIR.glob("*"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    reports = [
        report
        for report in reports
        if report.is_file()
    ]

    if not reports:
        print("\n[!] No reports found.")
        return

    latest = reports[0]

    print("\nLatest Report")
    print("-" * 70)
    print(f"File: {latest.name}")
    print()

    try:
        with open(
            latest,
            "r",
            encoding="utf-8"
        ) as file:
            print(file.read())

    except OSError as error:
        print(f"[!] Could not read report: {error}")


def search_reports():
    keyword = input(
        "\nEnter keyword to search: "
    ).strip().lower()

    if not keyword:
        print("\n[!] Search keyword cannot be empty.")
        return

    reports = [
        report
        for report in REPORT_DIR.glob("*")
        if report.is_file()
    ]

    matches = []

    for report in reports:
        try:
            content = report.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if keyword in content.lower():
                matches.append(report)

        except OSError:
            continue

    print("\nSearch Results")
    print("-" * 70)

    if not matches:
        print("[!] No matching reports found.")
        return

    for report in matches:
        print(f"[+] {report.name}")


def delete_report():
    reports = sorted(
        [
            report
            for report in REPORT_DIR.glob("*")
            if report.is_file()
        ],
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    if not reports:
        print("\n[!] No reports found.")
        return

    list_reports()

    choice = input(
        "\nEnter report number to delete: "
    ).strip()

    if not choice.isdigit():
        print("\n[!] Invalid selection.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(reports):
        print("\n[!] Report number out of range.")
        return

    selected = reports[index]

    confirm = input(
        f"Delete '{selected.name}'? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        print("\n[!] Delete cancelled.")
        return

    try:
        selected.unlink()
        print(f"\n[+] Deleted: {selected.name}")

    except OSError as error:
        print(f"\n[!] Could not delete report: {error}")


def clear_reports():
    reports = [
        report
        for report in REPORT_DIR.glob("*")
        if report.is_file()
    ]

    if not reports:
        print("\n[!] No reports found.")
        return

    confirm = input(
        f"\nDelete all {len(reports)} report(s)? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        print("\n[!] Clear operation cancelled.")
        return

    deleted = 0

    for report in reports:
        try:
            report.unlink()
            deleted += 1
        except OSError:
            pass

    print(f"\n[+] Deleted {deleted} report(s).")


def run():
    while True:
        print("\nReports Manager")
        print("-" * 40)
        print("[1] List Reports")
        print("[2] View Latest Report")
        print("[3] Search Reports")
        print("[4] Delete Report")
        print("[5] Clear Reports")
        print("[0] Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            list_reports()

        elif choice == "2":
            view_latest_report()

        elif choice == "3":
            search_reports()

        elif choice == "4":
            delete_report()

        elif choice == "5":
            clear_reports()

        elif choice == "0":
            break

        else:
            print("\n[!] Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run()
