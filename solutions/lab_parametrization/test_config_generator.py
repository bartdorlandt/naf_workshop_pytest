import pytest

from config_generator import generate_interface_config


@pytest.mark.parametrize(
    "interface,mode,vlan,expected_contains",
    [
        ("Ethernet1", "access", 10, "switchport access vlan 10"),
        ("Ethernet2", "trunk", 20, "switchport trunk allowed vlan 20"),
        ("Ethernet3", "access", 100, "switchport mode access"),
    ],
)
def test_interface_config(interface, mode, vlan, expected_contains):
    result = generate_interface_config(interface, mode, vlan)
    assert expected_contains in result


def test_unknown_mode_raises():
    with pytest.raises(ValueError, match="Unknown mode"):
        generate_interface_config("Ethernet1", "routed", 10)
