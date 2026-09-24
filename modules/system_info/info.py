import platform
import socket
import os


def run():
    print("\nSystem Information")
    print("-" * 30)

    print(f"OS: {platform.system()}")
    print(f"OS Release: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Cores: {os.cpu_count()}")


if __name__ == "__main__":
    run()
