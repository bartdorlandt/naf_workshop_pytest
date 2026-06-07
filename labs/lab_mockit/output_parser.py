def parse_ios_version(output: str) -> dict:
    """Parse 'show version' output.

    Returns a dict with keys: version (str), hostname (str), interfaces (int).
    Example: {'version': '16.9.3', 'hostname': 'csr1000v-1', 'interfaces': 3}
    """
    raise NotImplementedError("Implement this parser")


def parse_ip_interface_brief(output: str) -> list[dict]:
    """Parse 'show ip interface brief' output.

    Returns a list of dicts, one per interface, with keys:
    interface (str), ip (str), status (str), protocol (str).
    Example: [{'interface': 'Ethernet0/0', 'ip': 'unassigned', 'status': 'up', 'protocol': 'up'}]
    """
    raise NotImplementedError("Implement this parser")


def parse_bgp_summary(output: str) -> dict:
    """Parse 'show ip bgp summary' output.

    Returns a dict with keys: router_id (str), local_as (int), neighbors (list[dict]).
    Each neighbor dict has keys: neighbor (str), remote_as (int), state (str).
    Example: {'router_id': '10.0.0.0', 'local_as': 65000, 'neighbors': [...]}
    """
    raise NotImplementedError("Implement this parser")


def parse_ip_route(output: str) -> list[dict]:
    """Parse 'show ip route' output.

    Returns a list of dicts, one per route, with keys:
    code (str), network (str), via (str | None), interface (str | None).
    Example: [{'code': 'C', 'network': '10.10.20.0/24', 'via': None, 'interface': 'GigabitEthernet1'}]
    """
    raise NotImplementedError("Implement this parser")
