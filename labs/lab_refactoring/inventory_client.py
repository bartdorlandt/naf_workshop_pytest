"""
Network Inventory Client

Fetches active devices from a NetBox instance and returns a summary.

EXERCISE: Identify the anti-patterns that make this code hard to test.
"""

import requests

NETBOX_URL = "https://netbox.example.com"
NETBOX_TOKEN = "abc123secrettoken"


def get_active_devices_in_site(site_name):
    response = requests.get(
        f"{NETBOX_URL}/api/dcim/devices/",
        headers={"Authorization": f"Token {NETBOX_TOKEN}"},
        params={"site": site_name, "status": "active"},
    )
    response.raise_for_status()
    data = response.json()

    devices = []
    for device in data["results"]:
        devices.append({
            "name": device["name"],
            "ip": device["primary_ip"]["address"].split("/")[0] if device["primary_ip"] else None,
            "role": device["role"]["slug"],
            "site": device["site"]["slug"],
        })

    return devices


if __name__ == "__main__":
    devices = get_active_devices_in_site("munich")
    for d in devices:
        print(f"{d['name']} ({d['role']}) - {d['ip']}")
