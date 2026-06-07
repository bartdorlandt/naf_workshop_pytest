"""
VLAN Provisioning Script - Refactored

Business logic is separated from device interaction:
- validate_vlan_id()    -> pure function, no I/O
- generate_vlan_config() -> pure function, no I/O
- apply_vlan_config()   -> accepts device as parameter (dependency injection)
- provision_vlan()      -> orchestrates the above; requires a pre-built device
"""


def validate_vlan_id(vlan_id: int) -> None:
    if not 1 <= vlan_id <= 4094:
        raise ValueError(f"Invalid VLAN ID: {vlan_id}. Must be between 1 and 4094.")


def generate_vlan_config(vlan_id: int, vlan_name: str, interface: str) -> str:
    return f"""vlan {vlan_id}
   name {vlan_name}
!
interface {interface}
   switchport mode access
   switchport access vlan {vlan_id}
"""


def apply_vlan_config(device, config: str) -> None:
    device.load_merge_candidate(config=config)
    device.commit_config()


def provision_vlan(device, vlan_id: int, vlan_name: str, interface: str) -> None:
    validate_vlan_id(vlan_id)
    config = generate_vlan_config(vlan_id, vlan_name, interface)
    apply_vlan_config(device, config)


if __name__ == "__main__":
    from napalm import get_network_driver

    driver = get_network_driver("eos")
    device = driver("spine-01.example.com", "admin", "Sup3rS3cr3t!")
    device.open()
    provision_vlan(device, 100, "PROD_SERVERS", "Ethernet5")
    device.close()
