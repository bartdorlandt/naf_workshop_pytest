def get_device_hostname(device) -> str:
    """Get hostname from a device object."""
    facts = device.get_facts()
    return facts.get("hostname", "unknown")


def get_device_interfaces(device) -> dict:
    """Get interface details from a device object."""
    return device.get_interfaces()
