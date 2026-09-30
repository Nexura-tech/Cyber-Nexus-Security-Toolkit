from database.manager import (
    get_report_history,
    get_user_statistics,
)

from core.utils import (
    print_section,
    print_info,
    print_success,
    print_warning,
)


def show_user_statistics():
    """
    Display basic user security statistics.
    """

    statistics = get_user_statistics()

    print_section("User Security Statistics")

    print_info(
        f"Total Users    : "
        f"{statistics['total_users']}"
    )

    print_info(
        f"Active Users   : "
        f"{statistics['active_users']}"
    )

    print_info(
        f"Inactive Users : "
        f"{statistics['inactive_users']}"
    )

    print_info(
        f"Admin Users    : "
        f"{statistics['admin_users']}"
    )


def show_report_summary():
    """
    Display report statistics.
    """

    reports = get_report_history(1000)

    total_reports = len(reports)

    completed_reports = sum(
        1
        for report in reports
        if report["status"] == "completed"
    )

    failed_reports = sum(
        1
        for report in reports
        if report["status"] == "failed"
    )

    print_section("Report Summary")

    print_info(
        f"Total Reports      : {total_reports}"
    )

    print_info(
        f"Completed Reports  : {completed_reports}"
    )

    print_info(
        f"Failed Reports     : {failed_reports}"
    )


def show_recent_reports(limit=5):
    """
    Display the most recent generated reports.
    """

    reports = get_report_history(limit)

    print_section("Recent Reports")

    if not reports:
        print_warning(
            "No reports have been generated yet."
        )
        return

    for report in reports:

        print_info(
            f"ID      : {report['id']}"
        )

        print_info(
            f"Name    : {report['report_name']}"
        )

        print_info(
            f"Type    : {report['report_type']}"
        )

        print_info(
            f"Status  : {report['status']}"
        )

        print_info(
            f"Created : {report['created_at']}"
        )

        print("-" * 60)


def run():
    """
    Run the Security Dashboard.
    """

    show_user_statistics()

    show_report_summary()

    show_recent_reports()

    print_success(
        "Security Dashboard loaded successfully."
    )
