from modules.system_info.info import collect_system_info


def test_system_info_returns_dictionary():
    result = collect_system_info()

    assert isinstance(result, dict)


def test_system_info_contains_required_fields():
    result = collect_system_info()

    required_fields = [
        "os",
        "os_release",
        "architecture",
        "hostname",
        "python_version",
        "processor",
        "cpu_cores",
    ]

    for field in required_fields:
        assert field in result


def test_cpu_cores():
    result = collect_system_info()

    assert result["cpu_cores"] is None or result["cpu_cores"] > 0
