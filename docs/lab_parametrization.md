# LAB: Parametrization

## Objective

Use pytest parametrization to efficiently test multiple scenarios with minimal code duplication.

## Setup

The virtual env setup is only required if you haven't done so in the previous lab.

```bash
# from the root of this project
uv sync
source .venv/bin/activate
```
> Ensure your editor is aware of the virtual environment.

Continue in your lab directory or create a new one:

```bash
# from the root of this project
mkdir lab_parametrization
```

---

## Exercise 1: Basic Parametrization

!!! tip "Learning goals"
    - A single parametrized test replaces N near-identical test functions
    - `@pytest.mark.parametrize` receives a comma-separated string of argument names and a list of value tuples
    - Each tuple becomes one test case; pytest runs the test once per tuple

Create `lab_parametrization/validators.py` with two functions:

- `is_valid_vlan(vlan_id)` — returns `True` for IDs in range 1–4094
- `is_valid_hostname(hostname)` — returns `True` for names matching the pattern `^[a-z]{2,3}\d{2,3}$`

**Write tests** in `lab_parametrization/test_validators.py`. Here is the model:

```python
import pytest
from validators import is_valid_vlan, is_valid_hostname


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
```

Run your tests:

```bash
pytest -v lab_parametrization/test_validators.py
```

Observe how pytest names each case in the output — it uses the parameter values.

---

## Exercise 2: Parametrize with IDs

!!! tip "Learning goals"
    - `pytest.param(..., id=...)` gives a test case a human-readable name in the output
    - Descriptive IDs make failures immediately understandable without decoding raw values
    - IDs are especially useful when parameter values are objects, booleans, or long strings

Now add a parametrized test for `is_valid_hostname`. Here is the first case as a model — write the remaining four yourself:

```python
@pytest.mark.parametrize(
    "hostname,expected",
    [
        pytest.param("sw01", True, id="valid_switch"),
        # write the remaining cases here
    ],
)
def test_hostname_validation(hostname, expected):
    assert is_valid_hostname(hostname) == expected
```

Write cases for:

- A valid router hostname (3-letter prefix, 3 digits) — `id="valid_router"`
- An uppercase hostname — `id="uppercase_invalid"`
- A hostname with only one digit — `id="single_digit_invalid"`
- A hostname with a prefix longer than 3 letters — `id="too_long_prefix"`

Run again and compare the output with Exercise 1 — the IDs replace the raw values in the test names.

---

## Exercise 3: Multiple Parameters

!!! tip "Learning goals"
    - Parametrize works with any number of arguments — name them all in the first string
    - A separate non-parametrized test is the right place for error/exception cases
    - `pytest.raises(ValueError, match=...)` asserts both the type and the message

Create `lab_parametrization/config_generator.py` with a `generate_interface_config(interface, mode, vlan)` function that produces Cisco-style switchport config strings for `access` and `trunk` modes, and raises `ValueError` for unknown modes.

**Write tests** in `lab_parametrization/test_config_generator.py`. The error case is the model:

```python
import pytest
from config_generator import generate_interface_config


def test_unknown_mode_raises():
    with pytest.raises(ValueError, match="Unknown mode"):
        generate_interface_config("Ethernet1", "routed", 10)
```

Now write the parametrized test yourself:

- Function name: `test_interface_config`
- Parameters: `interface`, `mode`, `vlan`, `expected_contains`
- Write at least three cases covering both `access` and `trunk` modes across different interfaces
- Assert that `expected_contains` appears in the generated config string

Run your tests:

```bash
pytest -v lab_parametrization/test_config_generator.py
```

---

## Exercise 4: Load Test Data from YAML

!!! tip "Learning goals"
    - Test data in YAML keeps test files clean and makes adding cases trivial
    - A loader function returns a list of `pytest.param` objects, each with an `id` for readable output
    - `Path(__file__).parent` resolves paths relative to the test file, not the working directory

Add a `select_driver(vendor)` function to `config_generator.py` that maps vendor names (`"arista"`, `"cisco"`, `"juniper"`) to driver strings (`"eos"`, `"ios"`, `"junos"`).

Create `lab_parametrization/test_data.yaml` with a list of devices. Each device needs `hostname`, `vendor`, and `expected_driver` fields:

```yaml
devices:
  - hostname: sw01
    vendor: arista
    expected_driver: eos
  # add more devices here
```

**Write tests** in `lab_parametrization/test_from_yaml.py`. The loader helper is the model — write the test function yourself:

```python
from pathlib import Path
import pytest
import yaml
from config_generator import select_driver


def load_test_devices():
    data = yaml.safe_load((Path(__file__).parent / "test_data.yaml").read_text())
    return [pytest.param(d, id=d["hostname"]) for d in data["devices"]]


@pytest.mark.parametrize("device", load_test_devices())
def test_device_driver_selection(device):
    # call select_driver with the vendor from the device dict
    # assert the result matches expected_driver
```

Run your tests:

```bash
pytest -v lab_parametrization/test_from_yaml.py
```

Add a third device to `test_data.yaml` and re-run — observe that the new case appears automatically with no change to the test code.

---

## Checkpoint

!!! success "Solution"

    A complete solution for this lab is provided in the `solutions/lab_parametrization/` directory.
