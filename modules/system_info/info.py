import os
import platform
import socket

from core.reporter import save_json, save_text


def collect_system_info():
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "cpu_cores": os.cpu_count(),
    }


def display_system_info(info):
    print("\nSystem Information")
    print("-" * 40)

    print(f"OS:             {info['os']}")
    print(f"OS Release:     {info['os_release']}")
    print(f"Architecture:   {info['architecture']}")
    print(f"Hostname:       {info['hostname']}")
    print(f"Python Version: {info['python_version']}")
    print(f"Processor:      {info['processor']}")
    print(f"CPU Cores:      {info['cpu_cores']}")


def generate_reports(info):
    report_data = {
        "module": "System Information",
        "result": info,
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "System Information",
        "Operating System": info["os"],
        "OS Release": info["os_release"],
        "Architecture": info["architecture"],
        "Hostname": info["hostname"],
        "Python Version": info["python_version"],
        "Processor": info["processor"],
        "CPU Cores": info["cpu_cores"],
    }

    text_file = save_text(
        "Cyber Nexus System Information Report",
        text_data
    )

    return json_file, text_file


def run():
    print("\nSystem Information")
    print("-" * 30)

    info = collect_system_info()

    display_system_info(info)

    json_file, text_file = generate_reports(info)

    print("\nReports Generated")
    print("-" * 40)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
