---
marp: true
# theme: gaia
_class: lead
# paginate: true
# backgroundColor: #ffffff
style: |
    @import "default";
    @import "schema";
    @import "structure";

    :root {
        --base: #0d0d12;
        --surface: #171821;
        --overlay: #1f202d;
        --muted: #8b8b99;
        --subtle: #b5b5c4;
        --text: #f7f3d5;
        --accent: #ffdd57;
        --gold: #ffd166;
        --yellow: #ffe066;
        --amber: #f9a825;
        --blue: #7dcff6;
        --green: #8bd7a9;
        --highlight-low: #13141c;
        --highlight-muted: #252740;
        --highlight-high: #343850;

        font-family: Pier Sans, ui-sans-serif, system-ui, -apple-system,
            BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans,
            sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol,
            "Noto Color Emoji";
        font-weight: initial;

        background-color: var(--base);
    }
    /*Common style*/
    h1 {
        color: var(--accent);
        padding-bottom: 2mm;
        margin-bottom: 12mm;
    }
    h2 {
        color: var(--gold);
    }
    h3 {
        color: var(--gold);
    }
    h4 {
        color: var(--gold);
    }
    h5 {
        color: var(--gold);
    }
    h6 {
        color: var(--gold);
    }
    a {
        color: var(--blue);
    }
    p {
        font-size: 20pt;
        font-weight: 600;
        color: var(--text);
    }
    code {
        color: var(--text);
        background-color: var(--highlight-muted);
    }
    text {
        color: var(--text);
    }
    ul {
        color: var(--subtle);
    }
    li {
        color: var(--subtle);
    }
    img {
        background-color: var(--highlight-low);
    }
    strong {
        color: var(--text);
        font-weight: inherit;
        font-weight: 800;
    }
    mjx-container {
        color: var(--text);
    }
    marp-pre {
        background-color: var(--overlay);
        border-color: var(--highlight-high);
    }

    /*Code block*/
    .hljs-comment {
        color: var(--muted);
    }
    .hljs-attr {
        color: var(--green);
    }
    .hljs-punctuation {
        color: var(--subtle);
    }
    .hljs-string {
        color: var(--gold);
    }
    .hljs-title {
        color: var(--yellow);
    }
    .hljs-keyword {
        color: var(--amber);
    }
    .hljs-variable {
        color: var(--text);
    }
    .hljs-literal {
        color: var(--accent);
    }
    .hljs-type {
        color: var(--blue);
    }
    .hljs-number {
        color: var(--gold);
    }
    .hljs-built_in {
        color: var(--accent);
    }
    .hljs-params {
        color: var(--blue);
    }
    .hljs-symbol {
        color: var(--green);
    }
    .hljs-meta {
        color: var(--subtle);
    }
    .hljs-subst {
        color: var(--blue);
    }
---

# "It Works on My Machine"
## (Py)Test your Automation

**Proctors**: Urs Baumann, Steinn Orvar Bjarnarson, Bart Dorlandt

*NAF Workshop @ AutoCon5 — WS:B4*

---


# Admin

## Wi-Fi & Connectivity
- Network Name: `AutoCon5`
- Password: `MunichRocks!`

## Resources
- Docs: [https://bartdorlandt.github.io/naf_workshop_pytest/](https://bartdorlandt.github.io/naf_workshop_pytest/)
- Repo: [https://github.com/bartdorlandt/naf_workshop_pytest](https://github.com/bartdorlandt/naf_workshop_pytest)

---

# Setup

- `git clone https://github.com/bartdorlandt/naf_workshop_pytest.git`
- `cd naf_workshop_pytest`
- Install dependencies with one of the options:
  - `uv sync` || `task init`
- `source .venv/bin/activate` + IDE setup

---
<!-- 
# Setup without UV (not recommended)

If you really don't like UV or can not install it:

> Use Python 3.12

```bash
python3 -m venv .venv
cat << EOF >> pyproject.toml

[tool.setuptools]
py-modules = []
EOF
.venv/bin/pip install --require-virtualenv .
```

--- -->

# The Problem

> "I tested it locally and it broke in production"

**Common challenges in network automation:**
- Testing automation requires real devices or labs
- Network labs are expensive and unavailable
- Manual testing leads to errors
- Hard to test edge cases (timeouts, failures)
- No confidence when refactoring code

---

# Why Testing Matters

Testing enables **reliable automation** at scale:

✅ Catch errors before deployment
✅ Refactor with confidence
✅ Document expected behavior
✅ Enable CI/CD pipelines
✅ Reduce deployment risk

**Key insight:** Test automation logic locally, not on production devices.

---

# What We'll Cover

1. **Designing Testable Code** — Separation of concerns, dependency injection
2. **PyTest Fundamentals** — Simple, powerful testing framework
3. **Fixtures** — Setup, teardown, and test isolation
4. **Mocking** — Mock devices, APIs, and simulate failures
5. **Parametrization** — Data-driven testing
6. **CI/CD Integration** — Automate test runs in pipelines

---

# Why PyTest?

**PyTest is the go-to testing framework for Python:**

- **Simple syntax** — Just use `assert` statements
- **Powerful fixtures** — Setup/teardown and dependency injection
- **Great mocking** — Built-in support via `pytest-mock`
- **Parametrization** — Test multiple scenarios easily
- **CI/CD friendly** — Integrates with GitHub Actions, GitLab CI, etc.
- **Community** — Widely used, well-documented

---

# Why PyTest?

```python
def test_interface_config():
    config = generate_interface_config("eth0", "10.0.0.1")
    assert "interface eth0" in config
    assert "10.0.0.1" in config
```

---

# Assert Statements

> Assert statements provide clear, descriptive error messages:

```python
assert condition, "Error message if condition is False"
```

**Examples:**

```python
assert "10.0.0.1" in config, "IP address not found in config"
assert len(devices) > 0, "Expected at least one device"
assert device.is_connected(), "Device should be connected"
```

---

# Detailed failure output

```
================================= FAILURES =================================
______________________________ test_function _______________________________

    def test_function():
>       assert f() == 4
E       assert 3 == 4
E        +  where 3 = f()

test_assert1.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_assert1.py::test_function - assert 3 == 4
============================ 1 failed in 0.12s =============================
```

---

# Test Discovery

- Start: `testpaths` (default: cwd)
- Recurse into directories
- Search for `test_*.py` or `*_test.py` files
- From those files, collect test items:
  - `test` prefixed test functions or methods outside of class.
  - `test` prefixed test functions or methods inside `Test` prefixed test classes

<!-- 
https://docs.pytest.org/en/latest/explanation/goodpractices.html#conventions-for-python-test-discovery

-->
---

# Workshop Goal

Build **maintainable, scalable automation systems** by testing business logic locally without real devices.

**You will learn to:**
- Write testable automation code from the start
- Mock external dependencies (devices, APIs)
- Simulate failure scenarios
- Integrate testing into automation pipelines

---

# Tightly Coupled Code ❌

```python
from napalm import get_network_driver

def configure_interface(hostname, interface, ip_address):
    driver = get_network_driver("eos")
    device = driver(hostname, "admin", "password")
    device.open()

    config = f"""
    interface {interface}
        ip address {ip_address}
    """
    device.load_merge_candidate(config=config)
    device.commit_config()
    device.close()
```

---

# Tightly Coupled Code ❌

**Problems:**
- ❌ Requires real device to test
- ❌ Credentials hardcoded
- ❌ Business logic mixed with device interaction
- ❌ Hard to test edge cases

---

# The Solution: Separation of Concerns ✅

### 1. Pure Business Logic

```python
def generate_interface_config(interface: str, ip_address: str) -> str:
    """Generate interface configuration - testable without devices."""
    return f"""
interface {interface}
    ip address {ip_address}
"""
```

### 2. Device Interaction Layer

```python
def apply_config(device, config: str) -> bool:
    """Apply configuration - device is injected."""
    device.load_merge_candidate(config=config)
    device.commit_config()
    return True
```

---

# The Solution: Separation of Concerns ✅

✅ Business logic isolated → Easy to test
✅ Dependencies injected → Easy to mock

---

# Testable Architecture

```
┌──────────────────────────────────────────────┐
│         Business Logic Layer                 │
│  ✓ Config generation & validation            │
│  ✓ Pure functions, no side effects           │
│  ✓ Easy to unit test                         │
└──────────────────────────────────────────────┘
         ↓ (clean interface)
┌──────────────────────────────────────────────┐
│      Device Abstraction Layer                │
│  ✓ Dependency injection                      │
│  ✓ Works with real or mock devices           │
│  ✓ Error handling                            │
└──────────────────────────────────────────────┘
         ↓ (pluggable)
┌──────────────────────────────────────────────┐
│   Real Devices  │  Mock Devices  │  Stubs    │
│   (production)  │   (testing)    │ (CI/CD)   │
└──────────────────────────────────────────────┘
```

---
# Lab - Refactoring for Testability
---


# Fixtures: Reusable Test Setup

**Fixtures** are functions that provide test data or setup/teardown logic.

```python
import pytest

@pytest.fixture
def mock_device():
    """Fixture: Mock device for testing."""
    device = MagicMock()
    device.is_connected.return_value = True
    yield device  # Provide to test
    # Cleanup happens after test

def test_apply_config(mock_device):
    """Test uses the mock_device fixture."""
    result = apply_config(mock_device, "interface eth0...")
    assert result is True
    mock_device.load_merge_candidate.assert_called_once()
```

---

# Fixture Scopes

Fixtures have different lifespans:

| Scope      | Lifetime           | Use Case              |
| ---------- | ------------------ | --------------------- |
| `function` | Per test (default) | Fresh state each test |
| `class`    | Per test class     | Shared within class   |
| `module`   | Per file           | Expensive setup       |
| `session`  | Entire test run    | Global resources      |

---

# Fixture Scopes

```python
@pytest.fixture(scope="module")
def expensive_resource():
    """Created once per test module."""
    yield setup_expensive_thing()

@pytest.fixture(scope="function")
def fresh_state():
    """Created before each test."""
    yield create_fresh_state()
```

---
# Lab - Working with Fixtures
---
# Demo - Debug in VSCode
---

# Mocking Explained

**Why mock?**
- 🚀 Tests run **fast** (no device latency)
- 🔒 Tests are **isolated** (no real network)
- 🎯 Tests are **deterministic** (same result every time)
- 💥 Easy to **simulate failures** (timeouts, errors)

**What to mock:**
- Device drivers (NAPALM, Netmiko, etc.)
- Third-party APIs (REST, gRPC)
- External services (databases, caches)

**Don't mock:** Pure business logic that you're testing

---

# Mocking Strategies

### 1. Mock Device Drivers

```python
@pytest.fixture
def mock_napalm_device(mocker):
    device = mocker.MagicMock()
    device.get_facts.return_value = {"hostname": "router1"}
    return device

def test_get_device_facts(mock_napalm_device):
    facts = mock_napalm_device.get_facts()
    assert facts["hostname"] == "router1"
```

---

# Mocking Strategies

### 2. Simulate Failures

```python
def test_retry_on_timeout(mocker):
    device = mocker.MagicMock()
    device.open.side_effect = [TimeoutError(), None]  # Fail, then succeed

    # Your retry logic should handle this
    assert retry_connect(device) is True
```

---

# Common Mocking Patterns

```python
# Setup return values
mock_device.get_facts.return_value = {"os": "eos"}

# Track calls
mock_device.config.assert_called_once_with("set hostname router1")

# Verify arguments
mock_device.config.assert_called_with("interface eth0...")

# Simulate exceptions
mock_device.open.side_effect = AuthenticationError("Bad password")

# Multiple calls
mock_device.config.side_effect = [True, False, True]
```

---
# Lab - Mocking
---

# Data-Driven Testing

**Parametrization** lets you test multiple scenarios without code duplication:

```python
@pytest.mark.parametrize("interface,ip", [
    ("eth0", "10.0.0.1"),
    ("eth1", "10.0.0.2"),
    ("eth2", "192.168.1.1"),
])
def test_interface_configs(interface, ip):
    config = generate_interface_config(interface, ip)
    assert f"interface {interface}" in config
    assert ip in config
```


---

# Data-Driven Testing

**Benefits:**
- ✅ Test multiple cases with one function
- ✅ Clear which case fails
- ✅ Easy to add new test cases
- ✅ Reduced code duplication

---
# Lab - Parametrization
---

# CI/CD Integration

**Run tests automatically in pipelines:**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --tb=short --junit-xml=results.xml
      - uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: results.xml
```

---

# CI/CD Integration

**Outcomes:**
- ✅ Tests run on every commit
- ✅ Fail before merge to main
- ✅ Track test results over time

---
# Demo - CI/CD
---

# Best Practices Recap

1. **Write testable code from the start**
   - Separate business logic from device interaction
   - Use dependency injection

2. **Test business logic, mock external dependencies**
   - Fast, reliable, deterministic tests

3. **Use fixtures for reusability**
   - Setup/teardown, scope appropriately

---

# Best Practices Recap

4. **Parametrize for coverage**
   - Multiple scenarios, minimal code

5. **Integrate into CI/CD**
   - Tests run automatically, catch issues early

6. **Simulate failure scenarios**
   - Timeouts, errors, edge cases

---

# Questions?

**Let's build reliable automation together.**

- Proctors: Ready to help anytime
- Feedback: Welcomed!

**Thank you!**

---

# Links

- PyTest Documentation
  [https://docs.pytest.org/en/latest](https://docs.pytest.org/en/latest)
- PyTest Tips and Tricks
  [https://pyte.st/ref.pdf](https://pyte.st/ref.pdf)
- PyTest Plugins
  [https://docs.pytest.org/en/stable/reference/plugin_list.html](https://docs.pytest.org/en/stable/reference/plugin_list.html)


---

# Infrastructure Dependencies

- Testcontainer
  [https://testcontainers.com/](https://testcontainers.com/)
  [https://testcontainers-python.readthedocs.io/](https://testcontainers-python.readthedocs.io/)
- cisshgo
  [https://github.com/tbotnz/cisshgo](https://github.com/tbotnz/cisshgo)
- Mock'it
  [https://slurpit.io/mockit/](https://slurpit.io/mockit/)
  
---

# Testing Templates

- Infrahub SDK contains a PyTest plugin to test jinja2 templates
  https://docs.infrahub.app/testing-framework/overview

