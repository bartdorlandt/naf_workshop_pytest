import re


def is_valid_vlan(vlan_id: int) -> bool:
    """Check if VLAN ID is valid (1-4094)."""
    return 1 <= vlan_id <= 4094


def is_valid_hostname(hostname: str) -> bool:
    """Check if hostname follows naming convention."""
    pattern = r"^[a-z]{2,3}\d{2,3}$"
    return bool(re.match(pattern, hostname))
