# Mocking

## Why Mock?

In network automation, we often interact with:

- Network devices (SSH, NETCONF, APIs)
- External APIs (IPAM, CMDB, ticketing systems)
- Databases
- File systems

Mocking allows us to:

- Test without real devices
- Simulate error conditions
- Control test behavior precisely
- Run tests quickly and reliably

## unittest.mock Basics

Python's `unittest.mock` provides the core mocking functionality:

```python
from unittest.mock import Mock, MagicMock, patch

# Create a mock object
mock_device = Mock()

# Configure return values
mock_device.get_facts.return_value = {
    "hostname": "switch01",
    "vendor": "Arista"
}

# Use the mock
result = mock_device.get_facts()
assert result["hostname"] == "switch01"

# Verify calls
mock_device.get_facts.assert_called_once()
```

Documentation: [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)


## pytest-mock

The `pytest-mock` plugin provides a `mocker` fixture that integrates cleanly with pytest:

```python
def test_device_connection(mocker):
    # Patch a function
    mock_connect = mocker.patch("mymodule.connect_to_device")
    mock_connect.return_value = Mock(hostname="switch01")

    # Your test code here
    result = connect_and_get_hostname()

    assert result == "switch01"
    mock_connect.assert_called_once()
```

Documentation: [pytest-mock](https://pytest-mock.readthedocs.io/)

## Mocking Device Drivers

### Example: Mocking NAPALM

```python
from unittest.mock import Mock, patch

def test_get_device_facts(mocker):
    # Create a mock device
    mock_device = Mock()
    mock_device.get_facts.return_value = {
        "hostname": "switch01",
        "vendor": "Arista",
        "model": "cEOS",
        "uptime": 86400
    }

    # Patch the driver
    mock_driver = mocker.patch("napalm.get_network_driver")
    mock_driver.return_value.return_value = mock_device

    # Test your function
    from mymodule import get_device_info
    result = get_device_info("192.168.1.1")

    assert result["hostname"] == "switch01"
```

## Simulating Failures

### Timeout Errors

```python
from unittest.mock import Mock
from socket import timeout

def test_connection_timeout(mocker):
    mock_connect = mocker.patch("mymodule.connect_to_device")
    mock_connect.side_effect = timeout("Connection timed out")

    with pytest.raises(timeout):
        connect_to_device("192.168.1.1")
```

### Authentication Errors

```python
def test_auth_failure(mocker):
    mock_device = Mock()
    mock_device.open.side_effect = Exception("Authentication failed")

    # Test that your code handles auth failures gracefully
```

### Partial Configuration Push

```python
def test_partial_config_failure(mocker):
    mock_device = Mock()
    mock_device.load_merge_candidate.return_value = None
    mock_device.commit_config.side_effect = Exception(
        "Config commit failed: interface Ethernet5 does not exist"
    )

    # Test rollback behavior
```

## Mocking External APIs

```python
def test_ipam_lookup(mocker):
    mock_response = Mock()
    mock_response.json.return_value = {
        "ip": "192.168.1.1",
        "hostname": "switch01",
        "location": "DC1"
    }
    mock_response.status_code = 200

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response

    result = lookup_device_in_ipam("192.168.1.1")
    assert result["location"] == "DC1"
```

## monkeypatch

pytest's built-in `monkeypatch` fixture is a lightweight alternative to `unittest.mock` for replacing attributes, environment variables, and dictionary entries. All changes are automatically reverted after each test — no teardown needed.

### Environment Variables

```python
def test_uses_custom_api_url(monkeypatch):
    monkeypatch.setenv("API_URL", "https://staging.example.com")
    # Code that reads os.environ["API_URL"] will see the staging URL
```

### Replacing a Function or Attribute

```python
import network_utils

def test_get_device_uses_staging(monkeypatch):
    monkeypatch.setattr(network_utils.requests, "get", lambda *a, **kw: mock_response)
```

Patch at the same location the code imports from — the same rule as `mocker.patch`.

### Modifying a Dictionary

```python
def test_with_custom_config(monkeypatch):
    monkeypatch.setitem(config, "timeout", 5)
```

### Using monkeypatch in a Fixture

`monkeypatch` composes naturally with other fixtures, which is useful for setting up environment state shared across multiple tests:

```python
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("API_URL", "https://test.example.com")
    monkeypatch.setenv("API_TOKEN", "test-token")
```

### monkeypatch vs pytest-mock

|                 | `monkeypatch`                    | `pytest-mock` (`mocker`)                  |
| --------------- | -------------------------------- | ----------------------------------------- |
| Built-in        | Yes                              | Requires `pytest-mock`                    |
| Call assertions | No                               | Yes (`assert_called_once_with`)           |
| Best for        | Env vars, simple attribute swaps | Verifying interactions with external code |

## Best Practices

1. **Mock at the boundary** - Mock external interfaces, not internal logic
2. **Use spec** - `Mock(spec=RealClass)` ensures mock has same interface
3. **Verify interactions** - Use `assert_called_with()` to verify correct usage
4. **Don't over-mock** - If you're mocking everything, your test may not be valuable
