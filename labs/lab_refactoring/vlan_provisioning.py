"""
VLAN Provisioning Script

This script provisions a VLAN on a network device and assigns it to an interface.

EXERCISE: Identify the anti-patterns that make this code hard to test.
"""

from napalm import get_network_driver


def provision_vlan(hostname, vlan_id, vlan_name, interface):
    driver = get_network_driver("eos")
    device = driver(hostname, "admin", "Sup3rS3cr3t!")
    device.open()

    if not 1 <= vlan_id <= 4094:
        device.close()
        raise ValueError(f"Invalid VLAN ID: {vlan_id}")

    config = f"""vlan {vlan_id}
   name {vlan_name}
!
interface {interface}
   switchport mode access
   switchport access vlan {vlan_id}
"""

    device.load_merge_candidate(config=config)
    device.commit_config()
    print(f"VLAN {vlan_id} ({vlan_name}) provisioned on {hostname} interface {interface}")
    device.close()


if __name__ == "__main__":
    provision_vlan("spine-01.example.com", 100, "PROD_SERVERS", "Ethernet5")
