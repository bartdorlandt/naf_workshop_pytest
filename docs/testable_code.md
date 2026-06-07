# Designing Testable Code

## Why Testability Matters

Network automation scripts often start as quick solutions but grow into critical infrastructure. Without proper testing, changes become risky and debugging becomes time-consuming.

**Benefits of testable code:**

- Catch errors before deployment
- Refactor with confidence
- Document expected behavior
- Enable CI/CD pipelines

## The Problem: Tightly Coupled Code

Consider this common pattern in network automation:

(ignore the absence of error handling for now)

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

**Problems:**

- Cannot test without a real device
- Credentials hardcoded
- No error handling
- Business logic mixed with device interaction

## The Solution: Separation of Concerns

### 1. Separate Configuration Generation from Device Interaction

```python
def generate_interface_config(interface: str, ip_address: str) -> str:
    """Generate interface configuration - pure business logic."""
    return f"""
interface {interface}
    ip address {ip_address}
"""
```

This function can be tested without any device!

### 2. Use Dependency Injection

```python
def apply_config(device, config: str) -> bool:
    """Apply configuration to a device."""
    device.load_merge_candidate(config=config)
    device.commit_config()
    return True
```

The `device` is passed in, not created inside the function. This allows us to pass a mock device in tests. We'll focus on mocking in a later section.

### 3. Create a Testable Architecture

```
┌──────────────────────────────────────────────────┐
│              Business Logic                      │
│  (config generation, validation, decisions)      │
│                                                  │
│  ✓ Pure functions                                │
│  ✓ No external dependencies                      │
│  ✓ Easy to test                                  │
└──────────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│            Device Abstraction                    │
│  (interface for device operations)               │
│                                                  │
│  ✓ Dependency injection                          │
│  ✓ Mockable                                      │
└──────────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────┐
│           Device Implementation                  │
│  (NAPALM, Netmiko, API clients)                  │
│                                                  │
│  ✗ Hard to unit test                             │
│  ✓ Integration test with real devices            │
└──────────────────────────────────────────────────┘
```

## Key Principles

1. **Pure Functions**: Functions that only depend on their inputs and produce predictable outputs
2. **Dependency Injection**: Pass dependencies (like device connections) as parameters
3. **Single Responsibility**: Each function does one thing well
4. **Interface Segregation**: Define clear boundaries between layers
