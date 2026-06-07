"""
Configuration Backup Script

Connects to a device, retrieves the running config, and saves it to disk.

EXERCISE: Identify the anti-patterns that make this code hard to test.
"""

import os
from datetime import datetime

from napalm import get_network_driver

BACKUP_DIR = "/var/backups/network"


def backup_device_config(hostname):
    driver = get_network_driver("eos")
    device = driver(hostname, "admin", "Sup3rS3cr3t!")
    device.open()

    config = device.get_config()["running"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BACKUP_DIR}/{hostname}_{timestamp}.cfg"
    os.makedirs(BACKUP_DIR, exist_ok=True)

    with open(filename, "w") as f:
        f.write(config)

    print(f"Config saved to {filename}")
    device.close()
    return filename


if __name__ == "__main__":
    for host in ["spine-01.example.com", "spine-02.example.com", "leaf-01.example.com"]:
        backup_device_config(host)
