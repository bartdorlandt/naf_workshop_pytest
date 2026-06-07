from netmiko import ConnectHandler, BaseConnection


def get_connection(host: str, port: int, username: str, password: str) -> BaseConnection:
    """Return a Netmiko ConnectHandler connected to a cisco_ios device."""
    raise NotImplementedError("Implement this using netmiko.ConnectHandler")


def send_command(connection: BaseConnection, command: str) -> str:
    """Send a CLI command and return the output as a string."""
    raise NotImplementedError("Implement this using connection.send_command()")
