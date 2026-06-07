def test_inventory_count(expensive_inventory):
    assert len(expensive_inventory["devices"]) == 3


def test_inventory_has_sw1(expensive_inventory):
    assert "sw1" in expensive_inventory["devices"]
