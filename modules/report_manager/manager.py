from core.config import REPORT_DIR
from database.manager import (
    get_report_history,
    get_report_by_file_path,
    update_report_status,
)

def get_reports():
    """Return available report files sorted by newest first."""
    reports = [
        report
        for report in REPORT_DIR.glob("*")
        if report.is_file()
    ]

    return sorted(
        reports,
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )


def list_reports():
    """Display all available reports."""
    reports = get_reports()

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
    """Display the newest report."""
    reports = get_reports()

    if not reports:
        print("\n[!] No reports found.")
        return

    latest = reports[0]

    print("\nLatest Report")
    print("-" * 70)
    print(f"File: {latest.name}")
    print()

    try:
        print(
            latest.read_text(
                encoding="utf-8",
                errors="replace",
            )
        )

    except OSError as error:
        print(f"[!] Could not read report: {error}")


def search_reports():
    """Search report contents for a keyword."""
    keyword = input(
        "\nEnter keyword to search: "
    ).strip().lower()

    if not keyword:
        print("\n[!] Search keyword cannot be empty.")
        return

    reports = get_reports()
    matches = []

    for report in reports:
        try:
            content = report.read_text(
                encoding="utf-8",
                errors="ignore",
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
    """Delete one selected report and update its database status."""
    reports = get_reports()

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
        selected_path = str(
            selected.resolve()
        )

        report = get_report_by_file_path(
            selected_path
        )

        selected.unlink()

        if report is not None:
            update_report_status(
                report["id"],
                "deleted",
            )

            print(
                "[+] Report history updated: deleted"
            )
        else:
            print(
                "[!] Report history entry not found."
            )

        print(
            f"\n[+] Deleted: {selected.name}"
        )

    except OSError as error:
        print(
            f"\n[!] Could not delete report: {error}"
        )



def clear_reports():
    """Delete all generated reports after confirmation."""
    reports = get_reports()

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

def show_report_history():
    """Display report history stored in the database."""
    history = get_report_history()

    print("\nReport History")
    print("-" * 80)

    if not history:
        print("[!] No report history found.")
        return

    for report in history:
        print(f"ID:          {report['id']}")
        print(f"Name:        {report['report_name']}")
        print(f"Type:        {report['report_type']}")
        print(f"Created At:  {report['created_at']}")
        print(f"Status:      {report['status']}")
        print(f"File Path:   {report['file_path']}")
        print("-" * 80)

def run():
    """Run the Reports Manager menu."""
    while True:
        print("\nReports Manager")
        print("-" * 40)

        print("[1] List Reports")
        print("[2] View Latest Report")
        print("[3] Search Reports")
        print("[4] Delete Report")
        print("[5] Clear Reports")
        print("[6] Report History")
        print("[0] Back")

        choice = input(
            "\nSelect an option: "
        ).strip()

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

        elif choice == "6":
            show_report_history()

        elif choice == "0":
            break

        else:
            print("\n[!] Invalid option.")

        input(
            "\nPress Enter to continue..."
        )


if __name__ == "__main__":
    run()
