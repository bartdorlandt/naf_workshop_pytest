"""
Device Registry - Refactored

Business logic is separated from database interaction:
- build_device_record()  -> pure function, no I/O
- add_device()           -> accepts a connection as parameter; uses parameterized queries
- get_devices_for_site() -> accepts a connection as parameter; uses parameterized queries
"""

import sqlite3


def build_device_record(row: tuple) -> dict | None:
    hostname, ip_address, device_type, site = row
    if not ip_address:
        return None
    return {
        "hostname": hostname,
        "ip": ip_address,
        "type": device_type,
        "site": site,
    }


def add_device(
    conn: sqlite3.Connection,
    hostname: str,
    ip_address: str,
    device_type: str,
    site: str,
) -> None:
    conn.execute(
        "INSERT INTO devices (hostname, ip_address, device_type, site) VALUES (?, ?, ?, ?)",
        (hostname, ip_address, device_type, site),
    )
    conn.commit()


def get_devices_for_site(conn: sqlite3.Connection, site: str) -> list:
    cursor = conn.execute(
        "SELECT hostname, ip_address, device_type, site FROM devices WHERE site = ?",
        (site,),
    )
    rows = cursor.fetchall()
    return [record for row in rows if (record := build_device_record(row)) is not None]


if __name__ == "__main__":
    DB_PATH = "/var/db/network_inventory.db"
    conn = sqlite3.connect(DB_PATH)
    add_device(conn, "leaf-01", "10.0.0.1", "switch", "amsterdam")
    devices = get_devices_for_site(conn, "amsterdam")
    conn.close()
    for d in devices:
        print(f"{d['hostname']} ({d['type']}) - {d['ip']} @ {d['site']}")
