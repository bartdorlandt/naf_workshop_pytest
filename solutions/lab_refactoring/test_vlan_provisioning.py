import pytest

from vlan_provisioning import generate_vlan_config, validate_vlan_id


class TestValidateVlanId:
    def test_valid_vlan_id(self):
        validate_vlan_id(100)  # should not raise

    def test_vlan_id_lower_boundary(self):
        validate_vlan_id(1)

    def test_vlan_id_upper_boundary(self):
        validate_vlan_id(4094)

    def test_vlan_id_zero_raises(self):
        with pytest.raises(ValueError, match="Invalid VLAN ID"):
            validate_vlan_id(0)

    def test_vlan_id_too_large_raises(self):
        with pytest.raises(ValueError, match="Invalid VLAN ID"):
            validate_vlan_id(4095)


class TestGenerateVlanConfig:
    def test_contains_vlan_id(self):
        config = generate_vlan_config(100, "PROD_SERVERS", "Ethernet5")
        assert "vlan 100" in config

    def test_contains_vlan_name(self):
        config = generate_vlan_config(100, "PROD_SERVERS", "Ethernet5")
        assert "PROD_SERVERS" in config

    def test_contains_interface(self):
        config = generate_vlan_config(100, "PROD_SERVERS", "Ethernet5")
        assert "interface Ethernet5" in config

    def test_contains_switchport_assignment(self):
        config = generate_vlan_config(100, "PROD_SERVERS", "Ethernet5")
        assert "switchport access vlan 100" in config
