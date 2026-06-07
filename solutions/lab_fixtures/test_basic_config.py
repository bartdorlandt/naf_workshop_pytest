def test_switch_has_vlans(switch_config):
    assert len(switch_config["vlans"]) == 3


def test_ethernet1_is_access(switch_config):
    assert switch_config["interfaces"]["Ethernet1"]["mode"] == "access"
