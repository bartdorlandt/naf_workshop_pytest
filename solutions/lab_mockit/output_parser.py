import re


def parse_ios_version(output: str) -> dict:
    """Parse 'show version' output.

    Returns a dict with keys: version (str), hostname (str), interfaces (int).
    """
    version = ""
    hostname = ""
    interfaces = 0

    for line in output.splitlines():
        m = re.search(r"Version (\d+\.\d+\.\d+),", line)
        if m:
            version = m.group(1)

        m = re.match(r"^(\S+)\s+uptime is", line)
        if m:
            hostname = m.group(1)

        m = re.search(r"(\d+) Gigabit Ethernet interfaces", line)
        if m:
            interfaces = int(m.group(1))

    return {"version": version, "hostname": hostname, "interfaces": interfaces}


def parse_ip_interface_brief(output: str) -> list[dict]:
    """Parse 'show ip interface brief' output.

    Returns a list of dicts with keys: interface, ip, status, protocol.
    """
    results = []
    for line in output.splitlines():
        # Skip the header line
        if line.startswith("Interface"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            results.append(
                {
                    "interface": parts[0],
                    "ip": parts[1],
                    "status": parts[4],
                    "protocol": parts[5],
                }
            )
    return results


def parse_bgp_summary(output: str) -> dict:
    """Parse 'show ip bgp summary' output.

    Returns a dict with keys: router_id (str), local_as (int), neighbors (list[dict]).
    Each neighbor has keys: neighbor (str), remote_as (int), state (str).
    """
    router_id = ""
    local_as = 0
    neighbors = []
    in_neighbor_table = False

    for line in output.splitlines():
        m = re.search(r"BGP router identifier (\S+), local AS number (\d+)", line)
        if m:
            router_id = m.group(1)
            local_as = int(m.group(2))

        if line.startswith("Neighbor"):
            in_neighbor_table = True
            continue

        if in_neighbor_table and line.strip():
            parts = line.split()
            if len(parts) >= 9 and re.match(r"^\d+\.\d+\.\d+\.\d+$", parts[0]):
                neighbor_ip = parts[0]
                remote_as = int(parts[2])
                # State/PfxRcd is the last field(s) — may be "Idle (Admin)" or a number
                state = " ".join(parts[8:])
                neighbors.append(
                    {"neighbor": neighbor_ip, "remote_as": remote_as, "state": state}
                )

    return {"router_id": router_id, "local_as": local_as, "neighbors": neighbors}


def parse_ip_route(output: str) -> list[dict]:
    """Parse 'show ip route' output.

    Returns a list of dicts with keys: code (str), network (str),
    via (str | None), interface (str | None).
    """
    results = []
    # Match lines like: "C        10.10.20.0/24 is directly connected, GigabitEthernet1"
    # or: "S*    0.0.0.0/0 [1/0] via 10.10.20.254, GigabitEthernet1"
    for line in output.splitlines():
        m = re.match(
            r"^([A-Za-z*]+)\s+(\d+\.\d+\.\d+\.\d+(?:/\d+)?)\s+(?:\[\S+\]\s+)?(?:via\s+(\S+),\s+)?(?:is directly connected,\s+)?(\S+)?",
            line.strip(),
        )
        if m:
            code = m.group(1).rstrip("*")
            network = m.group(2)
            via = m.group(3)
            iface = m.group(4)
            results.append(
                {"code": code, "network": network, "via": via, "interface": iface}
            )
    return results
