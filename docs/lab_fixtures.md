# LAB: Working with Fixtures

## Objective

Create and use pytest fixtures for common test scenarios in network automation.

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
mkdir lab_fixtures
```

## Exercise 1: Basic Fixtures

Create a `lab_fixtures/conftest.py` with a fixture that provides a sample switch configuration (hostname, vlans list, interfaces dict).

```python
{
    "hostname": "switch01",
    "vlans": [10, 20, 30],
    "interfaces": {
        "Ethernet1": {"mode": "access", "vlan": 10},
        "Ethernet2": {"mode": "trunk", "allowed_vlans": [10, 20, 30]},
    },
}
```

Write tests in `lab_fixtures/test_basic_config.py` that use this fixture to assert:

- The switch has the expected number of VLANs
- A specific interface is in access mode

## Exercise 2: Fixture with Cleanup

Create a `config_file` fixture that uses pytest's built-in `tmp_path` fixture to write a temporary YAML config file and yield its path. You can place the fixture in `lab_fixtures/conftest.py`, in the test file or a separate file and import it.

Example content for the YAML file:
```yaml
hostname: testdevice
interfaces:
  - name: Ethernet1
    ip: 192.168.1.1/24
```

Write tests that verify the file exists and has the expected content.

file: `lab_fixtures/test_cleanup.py`


## Exercise 3: Fixture Scope

Create an `expensive_inventory` fixture with `scope="module"` that prints a message when it's called and returns a dict of devices.

Write two tests that use this fixture. Run with `-v -s` to observe that the fixture is only called once for the module:

```bash
pytest -v -s lab_fixtures/
```

file: `lab_fixtures/test_scope.py`

Next, remove the scope argument and run again to see that the fixture is called for each test. The default scope is "function", meaning it runs once per test function.


## Exercise 4: Fixture Dependencies

Create a chain of three fixtures (in the `conftest.py` file) where each depends on the previous:

- `device_list` — returns a list of device names (switches and routers)
- `switches_only` — depends on `device_list`, filters to only switch devices
- `first_switch` — depends on `switches_only`, returns the first entry

Write a test that uses `first_switch` and asserts its value.

file: `lab_fixtures/test_dependencies.py`

## Checkpoint

!!! success "Solution"

    A complete solution for this lab is provided in the `solutions/lab_fixtures/` directory.
