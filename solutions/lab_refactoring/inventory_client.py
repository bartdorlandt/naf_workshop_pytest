"""
Network Inventory Client - Refactored

Business logic is separated from HTTP calls:
- transform_device_data() -> pure function, no I/O
- fetch_devices()         -> accepts an HTTP client as parameter (dependency injection)
"""

import requests

NETBOX_URL = "https://netbox.example.com"
NETBOX_TOKEN = "abc123secrettoken"


def transform_device_data(raw_devices: list) -> list:
    result = []
    for device in raw_devices:
        result.append(
            {
                "name": device["name"],
                "ip": device["primary_ip"]["address"].split("/")[0]
                if device["primary_ip"]
                else None,
                "role": device["role"]["slug"],
                "site": device["site"]["slug"],
            }
        )
    return result


def fetch_devices(
    client, base_url: str, site_name: str, status: str = "active"
) -> list:
    response = client.get(
        f"{base_url}/api/dcim/devices/",
        params={"site": site_name, "status": status},
    )
    response.raise_for_status()
    data = response.json()
    return data["results"]


if __name__ == "__main__":
    devices = fetch_devices(requests, NETBOX_URL, "munich")
    transformed_devices = transform_device_data(devices)
    for d in transformed_devices:
        print(f"{d['name']} ({d['role']}) - {d['ip']}")
