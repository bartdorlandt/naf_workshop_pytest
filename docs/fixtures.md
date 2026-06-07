# PyTest Fixtures

## What are Fixtures?

Fixtures are pytest's way of providing test dependencies. They help you:

- Set up test preconditions
- Share common setup across tests
- Clean up after tests
- Manage test scope and lifecycle

## Basic Fixture

```python
import pytest

@pytest.fixture
def sample_device_data():
    return {
        "hostname": "switch01",
        "ip": "192.168.1.1",
        "vendor": "arista",
        "interfaces": ["Ethernet1", "Ethernet2", "Ethernet3"]
    }

def test_device_has_hostname(sample_device_data):
    assert sample_device_data["hostname"] == "switch01"

def test_device_has_interfaces(sample_device_data):
    assert len(sample_device_data["interfaces"]) == 3
```

## Fixture Scope

Fixtures can have different scopes controlling when they're created and destroyed:

```python
@pytest.fixture(scope="function")  # Default - new for each test
def per_test_data():
    return {"counter": 0}

@pytest.fixture(scope="module")  # Shared across all tests in a module
def shared_config():
    return load_config()

@pytest.fixture(scope="session")  # Shared across entire test session
def expensive_resource():
    return create_expensive_resource()
```

| Scope      | Created                     | Destroyed                 |
| ---------- | --------------------------- | ------------------------- |
| `function` | Before each test            | After each test           |
| `class`    | Before first test in class  | After last test in class  |
| `module`   | Before first test in module | After last test in module |
| `session`  | Once per test session       | At end of session         |

## Fixture with Setup and Teardown

Use `yield` to provide cleanup:

```python
@pytest.fixture
def temp_config_file():
    # Setup
    filepath = Path("/tmp/test_config.yaml")
    filepath.write_text("hostname: test")

    yield filepath  # Provide the fixture value

    # Teardown
    filepath.unlink()  # Clean up after test
```

## Fixture Dependencies

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def device_inventory():
    return ["switch01", "switch02", "router01"]

@pytest.fixture
def first_device(device_inventory):
    return device_inventory[0]

def test_first_device(first_device):
    assert first_device == "switch01"
```

## conftest.py

Share fixtures across multiple test files by placing them in `conftest.py`:

```
tests/
├── conftest.py          # Shared fixtures
├── test_config.py
├── test_validation.py
└── test_deployment.py
```

```python
# conftest.py
import pytest

@pytest.fixture
def mock_inventory():
    return {
        "switches": ["sw1", "sw2"],
        "routers": ["r1"]
    }
```

The `conftest.py` contents are automatically loaded by pytest, before running any tests.
All test files in the same directory (and subdirectories) can use fixtures from `conftest.py`.

Fixtures can also be imported from other files like any Python function. However, if a fixture depends on another fixture, it needs to be imported as well, otherwise pytest will not be able to resolve the dependency.

## Built-in Fixtures

pytest provides useful built-in fixtures:

- `tmp_path` - Temporary directory unique to each test
- `capsys` - Capture stdout/stderr
- `caplog` - Capture log messages
- `monkeypatch` - Modify objects, dictionaries, or environment variables

Example using `tmp_path`:

```python
def test_with_temp_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("hostname: test")
    assert config_file.exists()
```

A complete list of built-in fixtures can be found in the [pytest documentation - Fixtures reference](https://docs.pytest.org/en/stable/reference/fixtures.html#fixtures).

Example using `caplog`:
```python
def test_generate_config_caplog(tmp_path, caplog) -> None:
    p = Path(tmp_path / "output.txt")
    first = f"Writing config file {p}"
    second = f"Config file {p} created"
    code.generate_config(p)
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].message == first
    assert caplog.records[1].message == second
```

`monkeypatch` is a powerful built-in fixture for temporarily replacing objects, environment variables, and attributes during a test. Because it overlaps closely with mocking, it is covered in depth in the [Mocking chapter](mocking.md#monkeypatch).
