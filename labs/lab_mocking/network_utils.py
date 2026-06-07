import os

import requests

_DEFAULT_API_URL = "https://api.example.com"


def get_api_url() -> str:
    return os.environ.get("API_URL", _DEFAULT_API_URL)


def get_device_from_api(device_id: str) -> dict:
    """Fetch a device record from the inventory API."""
    base_url = get_api_url()
    response = requests.get(f"{base_url}/devices/{device_id}")
    response.raise_for_status()
    return response.json()


def list_devices_for_site(site: str) -> list[dict]:
    """Fetch all devices for a given site from the inventory API."""
    base_url = get_api_url()
    response = requests.get(f"{base_url}/devices/", params={"site": site})
    response.raise_for_status()
    return response.json().get("results", [])
