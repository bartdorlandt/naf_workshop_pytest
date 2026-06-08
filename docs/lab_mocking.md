# LAB: Mocking

## Objective

Use mocking to test network automation code without real devices or external services.

## Setup

The virtual env setup is only required if you haven't done so in the previous lab.

```bash
# from the root of this project
uv sync
source .venv/bin/activate
```
> Ensure your editor is aware of the virtual environment.

Copy the mocking lab directory to your project root:

```bash
# from the root of this project
# copy the lab files to your working directory to work with a copy
cp -r labs/lab_mocking .
```

The lab directory contains three modules:

- `device_info.py` — two functions that call methods on a device driver object
- `network_utils.py` — functions that call an external inventory API via `requests`
- `mymodule.py` — connection and config-deploy logic with retry behaviour

---

## Exercise 1: Basic Mocking

!!! tip "Learning goals"
    - A `Mock` object accepts any method call and returns another `Mock` by default
    - Configure return values with `.return_value` to control what your code sees
    - Verify the mock was called with `.assert_called_once()`

Open `lab_mocking/device_info.py`. It contains two functions: `get_device_hostname(device)` and `get_device_interfaces(device)`. Both take a device driver object as a parameter — which means you can pass a `Mock` in tests instead of a real device.

**Write tests** in `lab_mocking/test_ex1_basic_mocking.py`. Here is the first test as a model:

```python
from unittest.mock import Mock
from device_info import get_device_hostname, get_device_interfaces


class TestGetDeviceHostname:
    def test_returns_hostname_from_facts(self):
        mock_device = Mock()
        mock_device.get_facts.return_value = {"hostname": "switch01"}

        result = get_device_hostname(mock_device)

        assert result == "switch01"
        mock_device.get_facts.assert_called_once()
```

Now write the remaining tests yourself:

- `TestGetDeviceHostname`: add a test for when `hostname` is absent from the facts dict
- `TestGetDeviceInterfaces`: a new class with one test — configure `get_interfaces` to return a dict with at least one interface entry, call `get_device_interfaces`, and assert the interface name is in the result

Run your tests:

```bash
pytest -v lab_mocking/test_ex1_basic_mocking.py
```

---

## Exercise 2: Mocking with pytest-mock

!!! tip "Learning goals"
    - `mocker.patch` replaces a name in the module under test for the duration of the test
    - Patch at the location the code imports from — `network_utils.requests.get`, not `requests.get`
    - Verify the correct URL was called with `.assert_called_once_with(...)`

Open `lab_mocking/network_utils.py`. The functions `get_device_from_api` and `list_devices_for_site` both call `requests.get` internally. Use `mocker.patch` to replace it.

**Write tests** in `lab_mocking/test_ex2_pytest_mock.py`. Here is the first test as a model:

```python
from network_utils import get_device_from_api, list_devices_for_site


class TestGetDeviceFromApi:
    def test_returns_device_data(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"id": "123", "hostname": "switch01"}
        mock_get = mocker.patch("network_utils.requests.get", return_value=mock_response)

        result = get_device_from_api("123")

        assert result["hostname"] == "switch01"
        mock_get.assert_called_once_with("https://api.example.com/devices/123")
```

Now write the remaining tests yourself:

- `TestGetDeviceFromApi`: add a test that verifies `raise_for_status` is called on the response
- `TestListDevicesForSite`: a new class — patch `requests.get` to return a response with two devices in `results`, call `list_devices_for_site("amsterdam")`, and assert the correct count is returned

Run your tests:

```bash
pytest -v lab_mocking/test_ex2_pytest_mock.py
```

---

## Exercise 3: Simulating Failures

!!! tip "Learning goals"
    - `.side_effect` on a mock makes it raise an exception when called
    - Use `pytest.raises()` to assert that the exception propagates out of your code
    - This lets you test error-handling paths without a real server or device

**Write tests** in `lab_mocking/test_ex3_simulating_failures.py`. Here is the first test as a model:

```python
import pytest
from network_utils import get_device_from_api


class TestSimulatingFailures:
    def test_connection_timeout_raises(self, mocker):
        from socket import timeout
        mocker.patch(
            "network_utils.requests.get",
            side_effect=timeout("Connection timed out"),
        )

        with pytest.raises(timeout):
            get_device_from_api("switch01")
```

Now write one more test yourself:

- Simulate an HTTP error: make `raise_for_status` raise `requests.HTTPError`, and assert it propagates

Run your tests:

```bash
pytest -v lab_mocking/test_ex3_simulating_failures.py
```

---

## Exercise 4: Testing Retry Logic

!!! tip "Learning goals"
    - Pass a list to `side_effect` to simulate a sequence of outcomes: each call consumes the next item
    - If an item in the list is an exception instance, the mock raises it; otherwise it returns it
    - This lets you test "fail twice, succeed on third attempt" without any real infrastructure

Open `lab_mocking/mymodule.py`. The `deploy_config` function calls `connect()` internally and retries up to 3 times on failure. Use `mocker.patch("mymodule.connect", ...)` to control what `connect` returns on each call.

**Write tests** in `lab_mocking/test_ex4_retry_logic.py`. The retry test is the new concept here — it's given in full:

```python
import pytest
from unittest.mock import Mock
from mymodule import deploy_config


class TestRetryLogic:
    def test_retries_on_transient_failure(self, mocker):
        mock_device = Mock()
        mock_connect = mocker.patch(
            "mymodule.connect",
            side_effect=[
                Exception("Connection failed"),
                Exception("Connection failed"),
                mock_device,
            ],
        )

        deploy_config("switch01", "interface Ethernet1\n  shutdown")

        assert mock_connect.call_count == 3
        mock_device.commit_config.assert_called_once()
```

Now write the remaining two tests yourself:

- A test that verifies `deploy_config` succeeds on the first attempt (no retries needed)
- A test that verifies a `RuntimeError` is raised after all retries are exhausted

Run your tests:

```bash
pytest -v lab_mocking/test_ex4_retry_logic.py
```

---

## Exercise 5: monkeypatch

!!! tip "Learning goals"
    - `monkeypatch.setenv` sets an environment variable for one test and restores it afterwards — no cleanup needed
    - `monkeypatch.setattr` replaces any attribute on any object, including `requests.get` on the `requests` module
    - An `autouse=True` fixture in `conftest.py` runs for every test in the directory without being named explicitly

Open `lab_mocking/network_utils.py` and find `get_api_url()`. It reads `API_URL` from the environment and falls back to a default. You'll write tests that control that variable with `monkeypatch`.

**Write tests** in `lab_mocking/test_ex5_monkeypatch.py`. Here is the first test as a model:

```python
import network_utils
from network_utils import get_api_url, get_device_from_api


class TestGetApiUrl:
    def test_returns_env_var_when_set(self, monkeypatch):
        monkeypatch.setenv("API_URL", "https://staging.example.com")
        assert get_api_url() == "https://staging.example.com"
```

Now write the remaining tests yourself:

- `TestGetApiUrl`: add a test for when `API_URL` is not set — use `monkeypatch.delenv("API_URL", raising=False)` and assert the default is returned
- `TestGetDeviceFromApiWithMonkeypatch`: a new class — use `monkeypatch.setattr(network_utils.requests, "get", ...)` to replace `requests.get` with a lambda or function, call `get_device_from_api`, and assert the result

**Create `lab_mocking/conftest.py`** with an `autouse` fixture so all tests in the directory get a known `API_URL`:

```python
import pytest


@pytest.fixture(autouse=True)
def default_api_url(monkeypatch):
    monkeypatch.setenv("API_URL", "https://api.example.com")
```

Run your tests:

```bash
pytest -v lab_mocking/test_ex5_monkeypatch.py
```

---

## Checkpoint

!!! success "Solution"

    A complete solution for this lab is provided in the `solutions/lab_mocking/` directory.
