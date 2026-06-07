"""
Device Registry

Stores and retrieves device records from a SQLite database.

EXERCISE: Identify the anti-patterns that make this code hard to test.
"""

import sqlite3

DB_PATH = "/var/db/network_inventory.db"


def add_device(hostname, ip_address, device_type, site):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        f"INSERT INTO devices (hostname, ip_address, device_type, site) "
        f"VALUES ('{hostname}', '{ip_address}', '{device_type}', '{site}')"
    )
    conn.commit()
    conn.close()


def get_devices_for_site(site):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(f"SELECT hostname, ip_address, device_type, site FROM devices WHERE site = '{site}'")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        if row[1]:  # only include devices with an IP address
            result.append({
                "hostname": row[0],
                "ip": row[1],
                "type": row[2],
                "site": row[3],
            })
    return result


if __name__ == "__main__":
    add_device("leaf-01", "10.0.0.1", "switch", "amsterdam")
    devices = get_devices_for_site("amsterdam")
    for d in devices:
        print(f"{d['hostname']} ({d['type']}) - {d['ip']} @ {d['site']}")
