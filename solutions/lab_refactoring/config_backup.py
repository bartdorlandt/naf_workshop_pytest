"""
Configuration Backup Script - Refactored

Business logic is separated from device and filesystem interaction:
- generate_backup_filename() -> pure function, no I/O
- write_backup()             -> accepts path and content; file I/O only
- fetch_running_config()     -> accepts device as parameter
- backup_device_config()     -> orchestrates the above
"""

import os
from datetime import datetime


def generate_backup_filename(
    hostname: str, timestamp: datetime, backup_dir: str
) -> str:
    ts = timestamp.strftime("%Y%m%d_%H%M%S")
    return os.path.join(backup_dir, f"{hostname}_{ts}.cfg")


def write_backup(filename: str, content: str) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)


def fetch_running_config(device) -> str:
    return device.get_config()["running"]


def backup_device_config(
    device, hostname: str, backup_dir: str, timestamp: datetime | None = None
) -> str:
    if timestamp is None:
        timestamp = datetime.now()
    config = fetch_running_config(device)
    filename = generate_backup_filename(hostname, timestamp, backup_dir)
    write_backup(filename, config)
    return filename


if __name__ == "__main__":
    from napalm import get_network_driver

    BACKUP_DIR = "/var/backups/network"
    for hostname in [
        "spine-01.example.com",
        "spine-02.example.com",
        "leaf-01.example.com",
    ]:
        driver = get_network_driver("eos")
        device = driver(hostname, "admin", "Sup3rS3cr3t!")
        device.open()
        filename = backup_device_config(device, hostname, BACKUP_DIR)
        device.close()
        print(f"Config saved to {filename}")
