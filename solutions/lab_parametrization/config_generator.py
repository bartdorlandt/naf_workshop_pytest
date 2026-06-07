def generate_interface_config(interface: str, mode: str, vlan: int) -> str:
    if mode == "access":
        return f"interface {interface}\n  switchport mode access\n  switchport access vlan {vlan}"
    elif mode == "trunk":
        return f"interface {interface}\n  switchport mode trunk\n  switchport trunk allowed vlan {vlan}"
    raise ValueError(f"Unknown mode: {mode}")


def select_driver(vendor: str) -> str:
    drivers = {
        "arista": "eos",
        "cisco": "ios",
        "juniper": "junos",
    }
    return drivers[vendor]
