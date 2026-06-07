import pytest
from device_connector import send_command
from output_parser import (
    parse_ios_version,
    parse_ip_interface_brief,
    parse_bgp_summary,
    parse_ip_route,
)


EXPECTED_COMMANDS = [
    "show version",
    "show ip interface brief",
    "show ip bgp summary",
    "show ip route",
]


@pytest.mark.parametrize("command", EXPECTED_COMMANDS)
def test_command_returns_output(ios_device, command):
    output = send_command(ios_device, command)
    assert isinstance(output, str)
    assert len(output) > 0


@pytest.mark.parametrize(
    "command, expected_substring",
    [
        ("show version", "IOS XE"),
        ("show ip interface brief", "Loopback0"),
        ("show ip bgp summary", "BGP router identifier"),
        ("show ip route", "Gateway of last resort"),
    ],
)
def test_command_output_contains_expected_text(ios_device, command, expected_substring):
    output = send_command(ios_device, command)
    assert expected_substring in output


@pytest.mark.parametrize(
    "parser, command, check",
    [
        (parse_ios_version, "show version", lambda r: r["version"] == "16.9.3"),
        (parse_ip_interface_brief, "show ip interface brief", lambda r: len(r) == 6),
        (parse_bgp_summary, "show ip bgp summary", lambda r: r["local_as"] == 65000),
        (parse_ip_route, "show ip route", lambda r: len(r) > 0),
    ],
    ids=["version", "interfaces", "bgp", "routes"],
)
def test_parser_produces_expected_result(ios_device, parser, command, check):
    output = send_command(ios_device, command)
    result = parser(output)
    assert check(result)
