import pytest

from validators import is_valid_hostname, is_valid_vlan


@pytest.mark.parametrize(
    "vlan_id,expected",
    [
        (1, True),
        (100, True),
        (4094, True),
        (0, False),
        (4095, False),
        (-1, False),
    ],
)
def test_vlan_validation(vlan_id, expected):
    assert is_valid_vlan(vlan_id) == expected


@pytest.mark.parametrize(
    "hostname,expected",
    [
        pytest.param("sw01", True, id="valid_switch"),
        pytest.param("rtr001", True, id="valid_router"),
        pytest.param("Switch01", False, id="uppercase_invalid"),
        pytest.param("sw1", False, id="single_digit_invalid"),
        pytest.param("switch01", False, id="too_long_prefix"),
    ],
)
def test_hostname_validation(hostname, expected):
    assert is_valid_hostname(hostname) == expected
