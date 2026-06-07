# LAB: Refactoring for Testability

The `labs/lab_refactoring/` directory contains four deliberately tightly coupled scripts. Each one demonstrates anti-patterns that make automated testing difficult:

| File                   | Anti-patterns                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- |
| `vlan_provisioning.py` | Device connection created inside the function; hardcoded credentials; config generation mixed with device I/O |
| `config_backup.py`     | Device connection, file I/O, and filename logic all combined; hardcoded credentials and path                  |
| `inventory_client.py`  | HTTP call and data transformation in the same function; hardcoded URL and token                               |
| `device_registry.py`   | Database connection created inside every function; SQL injection risk; query and transformation mixed         |

## Objective

Refactor tightly coupled automation scripts into clean, testable modules by separating business logic from external interactions.

## Setup

Ensure your virtual environment is set up and activated:

```bash
# from the root of this project
uv sync
source .venv/bin/activate

# copy the lab files to your working directory to work with a copy
cp -r labs/lab_refactoring .
```

Ensure your editor is aware of the virtual environment.

---

## Exercise 1: VLAN Provisioning

!!! tip "Learning goals"
    - Small, well-named functions are easier to read and easier to test
    - If a function does one thing, you know exactly what to assert
    - Testing pure functions requires no devices, no mocks — just inputs and outputs

Open `lab_refactoring/vlan_provisioning.py` and read through it.

**Identify the problems:**

1. Where is the VLAN ID validation? Could you test it without connecting to a device?
2. Where is the config string built? Could you test that without a real device?
3. What would happen if you called this function in a test suite?

**Refactor:** extract these two functions into your copy of `vlan_provisioning.py`:

```python
def validate_vlan_id(vlan_id: int) -> None:
    """Raise ValueError if vlan_id is outside the valid range 1–4094."""

def generate_vlan_config(vlan_id: int, vlan_name: str, interface: str) -> str:
    """Return the EOS config block as a string."""
```

**Write tests** in `lab_refactoring/test_vlan_provisioning.py`:

```python
import pytest
from vlan_provisioning import validate_vlan_id, generate_vlan_config


def test_validate_vlan_id_valid():
    validate_vlan_id(100)  # should not raise


def test_validate_vlan_id_out_of_range():
    with pytest.raises(ValueError):
        validate_vlan_id(0)


def test_generate_vlan_config_contains_vlan_id():
    config = generate_vlan_config(100, "PROD", "Ethernet1")
    assert "vlan 100" in config


def test_generate_vlan_config_contains_interface():
    config = generate_vlan_config(100, "PROD", "Ethernet1")
    assert "interface Ethernet1" in config
```

Run your tests:

```bash
pytest -v lab_refactoring/test_vlan_provisioning.py
```

> In this lab we'll not work on mocking the device connection, we'll come back to that later.

---

## Exercise 2: Config Backup

!!! tip "Learning goals"
    - Functions that call `datetime.now()` internally produce unpredictable output — impossible to assert against
    - Passing time as a parameter gives tests full control
    - The `tmp_path` fixture gives each test its own temporary directory, automatically cleaned up

Open `lab_refactoring/config_backup.py` and read through it.

**Identify the problems:**

1. `backup_device_config` does at least three distinct things — what are they?
2. If you wrote `assert "20240608" in filename`, would that ever reliably pass?
3. What does the function write to disk, and where?

**Refactor:** extract these two functions:

```python
def generate_backup_filename(hostname: str, timestamp: datetime, backup_dir: str) -> str:
    """Return the full backup filepath as a string."""

def write_backup(filename: str, content: str) -> None:
    """Write content to filename, creating parent directories as needed."""
```

**Write tests** in `lab_refactoring/test_config_backup.py`:

```python
from datetime import datetime
from pathlib import Path
from config_backup import generate_backup_filename, write_backup


def test_generate_backup_filename_contains_hostname():
    ts = datetime(2024, 6, 8, 14, 30, 0)
    result = generate_backup_filename("spine-01", ts, "/backups")
    assert "spine-01" in result


def test_generate_backup_filename_contains_timestamp():
    ts = datetime(2024, 6, 8, 14, 30, 0)
    result = generate_backup_filename("spine-01", ts, "/backups")
    assert "20240608_143000" in result


def test_write_backup_creates_file(tmp_path):
    filepath = str(tmp_path / "spine-01_backup.cfg")
    write_backup(filepath, "hostname spine-01")
    assert Path(filepath).read_text() == "hostname spine-01"
```

Run your tests:

```bash
pytest -v lab_refactoring/test_config_backup.py
```

Notice that because `timestamp` is a parameter, you pass a hardcoded `datetime` object. No randomness, no flakiness.

---

## Exercise 3: Inventory Client

!!! tip "Learning goals"
    - Passing the HTTP client as a parameter means tests never touch the network
    - Separating data fetching from data transformation lets you test the transformation logic with plain dicts
    - A factory helper function reduces repetition across many test cases

Open `lab_refactoring/inventory_client.py` and read through it.

**Identify the problems:**

1. To test `get_active_devices_in_site`, what would you need to set up? What could go wrong?
2. Could you test the transformation logic (building the dict with `name`, `ip`, `role`, `site`) without any HTTP call?

**Refactor:** split the function in two:

```python
def transform_device_data(raw_devices: list) -> list:
    """Convert raw NetBox device dicts to simplified dicts."""

def fetch_devices(client, base_url: str, site_name: str, status: str = "active") -> list:
    """Fetch raw device list from the API. client must have a .get() method."""
```

**Write tests** in `lab_refactoring/test_inventory_client.py`. Use a helper function to build test data without repeating yourself:

```python
from inventory_client import transform_device_data


def make_raw_device(name="leaf-01", ip="10.0.0.1/32", role="leaf", site="amsterdam"):
    return {
        "name": name,
        "primary_ip": {"address": ip},
        "role": {"slug": role},
        "site": {"slug": site},
    }


def test_transform_extracts_name():
    result = transform_device_data([make_raw_device(name="spine-01")])
    assert result[0]["name"] == "spine-01"


def test_transform_strips_cidr():
    result = transform_device_data([make_raw_device(ip="10.0.0.1/32")])
    assert result[0]["ip"] == "10.0.0.1"


def test_transform_handles_no_ip():
    device = make_raw_device()
    device["primary_ip"] = None
    result = transform_device_data([device])
    assert result[0]["ip"] is None
```

Run your tests:

```bash
pytest -v lab_refactoring/test_inventory_client.py
```

---

## Exercise 4: Device Registry

!!! warning "Stretch exercise"
    This exercise introduces SQL injection and in-memory databases. If you're short on time, come back to it after the other exercises.

!!! tip "Learning goals"
    - Building SQL queries with f-strings lets attackers control your database — parameterized queries prevent this
    - Passing the database connection as a parameter lets tests use an in-memory database: fast, isolated, no files left behind
    - A fixture that creates the in-memory DB and tears it down is the standard pattern for database tests

Open `lab_refactoring/device_registry.py` and read through it.

**Identify the problems:**

1. Find the two f-string SQL queries. What would happen if you passed `"amsterdam' OR '1'='1"` as the `site` argument?
2. What file on disk does the code write to on every call? What would happen to that file during a test run?

**Refactor:** extract three functions:

```python
def build_device_record(row: tuple) -> dict | None:
    """Return a dict from a DB row tuple, or None if IP is empty."""

def add_device(conn: sqlite3.Connection, hostname: str, ip_address: str, device_type: str, site: str) -> None:
    """Insert a device record using parameterized queries."""

def get_devices_for_site(conn: sqlite3.Connection, site: str) -> list:
    """Return devices for a site, excluding those without an IP."""
```

Use parameterized queries (`?` placeholders) instead of f-strings in `add_device` and `get_devices_for_site`.

**Write tests** in `lab_refactoring/test_device_registry.py`. The key is the `db` fixture — it creates a fresh in-memory database for each test:

```python
import sqlite3
import pytest
from device_registry import add_device, get_devices_for_site


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE devices (
            hostname TEXT, ip_address TEXT, device_type TEXT, site TEXT
        )
    """)
    yield conn
    conn.close()


def test_add_device_stores_record(db):
    add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
    rows = db.execute("SELECT hostname FROM devices").fetchall()
    assert rows[0][0] == "leaf-01"


def test_get_devices_excludes_no_ip(db):
    add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
    add_device(db, "leaf-02", "", "switch", "amsterdam")
    result = get_devices_for_site(db, "amsterdam")
    assert len(result) == 1
    assert result[0]["hostname"] == "leaf-01"
```

Run your tests:

```bash
pytest -v lab_refactoring/test_device_registry.py
```

---

## Checkpoint

!!! success "Solution"

    A complete solution for this lab is provided in the `solutions/lab_refactoring/` directory.
