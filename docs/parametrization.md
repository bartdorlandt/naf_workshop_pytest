# Parametrization

## Why Parametrize?

Instead of writing multiple similar tests, parametrization lets you run the same test with different inputs:

```python
import pytest


def is_valid_vlan(vlan_id) -> bool:
    return 1 <= vlan_id <= 4094


# Without parametrization - repetitive
def test_vlan_10_valid():
    assert is_valid_vlan(10) is True

def test_vlan_100_valid():
    assert is_valid_vlan(100) is True

def test_vlan_4094_valid():
    assert is_valid_vlan(4094) is True
```

Has the following output:

```python
test_bart.py::test_vlan_10_valid PASSED               [ 33%]
test_bart.py::test_vlan_100_valid PASSED              [ 66%]
test_bart.py::test_vlan_4094_valid PASSED             [100%]
```

```python
# With parametrization - clean and maintainable
@pytest.mark.parametrize("vlan_id", [10, 100, 4094])
def test_valid_vlans(vlan_id):
    assert is_valid_vlan(vlan_id) is True
```

Has output:

```python
test_bart.py::test_valid_vlans[10] PASSED             [ 33%]
test_bart.py::test_valid_vlans[100] PASSED            [ 66%]
test_bart.py::test_valid_vlans[4094] PASSED           [100%]
```

## Basic Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("192.168.1.1", True),
    ("10.0.0.1", True),
    ("256.1.1.1", False),
    ("not.an.ip", False),
])
def test_is_valid_ip(input, expected):
    assert is_valid_ip(input) == expected
```

## Multiple Parameters

```python
@pytest.mark.parametrize("hostname,vendor,expected_prompt", [
    ("switch01", "arista", "switch01#"),
    ("router01", "cisco", "router01#"),
    ("fw01", "juniper", "fw01>"),
])
def test_generate_prompt(hostname, vendor, expected_prompt):
    result = generate_prompt(hostname, vendor)
    assert result == expected_prompt
```

## Parametrize with IDs

Add readable test IDs:

```python
@pytest.mark.parametrize("vlan_id,expected", [
    pytest.param(1, True, id="minimum_vlan"),
    pytest.param(4094, True, id="maximum_vlan"),
    pytest.param(0, False, id="below_minimum"),
    pytest.param(4095, False, id="above_maximum"),
])
def test_vlan_validation(vlan_id, expected):
    assert is_valid_vlan(vlan_id) == expected
```

Output:
```
test_vlans.py::test_vlan_validation[minimum_vlan] PASSED
test_vlans.py::test_vlan_validation[maximum_vlan] PASSED
test_vlans.py::test_vlan_validation[below_minimum] PASSED
test_vlans.py::test_vlan_validation[above_maximum] PASSED
```

## Combining Parametrize Decorators

Multiple decorators create a cartesian product:

```python
@pytest.mark.parametrize("vendor", ["arista", "cisco", "juniper"])
@pytest.mark.parametrize("interface_type", ["ethernet", "loopback", "vlan"])
def test_interface_naming(vendor, interface_type):
    # Tests all 9 combinations
    result = get_interface_prefix(vendor, interface_type)
    assert result is not None
```

## Parametrize with Fixtures

Combine parametrization with fixtures using `indirect`:

```python
@pytest.fixture
def device_config(request):
    configs = {
        "minimal": {"hostname": "sw1"},
        "full": {"hostname": "sw1", "vlans": [10, 20], "interfaces": ["Eth1"]},
    }
    return configs[request.param]

@pytest.mark.parametrize("device_config", ["minimal", "full"], indirect=True)
def test_config_validation(device_config):
    assert "hostname" in device_config
```

## Real-World Example: Testing Multiple Devices

```python
DEVICE_TEST_CASES = [
    pytest.param(
        {"hostname": "switch01", "ip": "192.168.1.1", "vendor": "arista"},
        id="arista_switch"
    ),
    pytest.param(
        {"hostname": "router01", "ip": "192.168.1.2", "vendor": "cisco"},
        id="cisco_router"
    ),
    pytest.param(
        {"hostname": "fw01", "ip": "192.168.1.3", "vendor": "paloalto"},
        id="paloalto_firewall"
    ),
]

@pytest.mark.parametrize("device", DEVICE_TEST_CASES)
def test_device_connection_string(device):
    result = build_connection_string(device)
    assert device["hostname"] in result
    assert device["ip"] in result
```

## Best Practices

1. **Use descriptive IDs** - Makes test output readable
2. **Group related test cases** - Keep parametrize data organized
3. **Don't over-parametrize** - If tests need different assertions, write separate tests
4. **Consider data files** - For large datasets, load from YAML/JSON
