from netmiko import ConnectHandler, BaseConnection


def get_connection(
    host: str, port: int, username: str, password: str
) -> BaseConnection:
    """Return a Netmiko ConnectHandler connected to a cisco_ios device."""
    return ConnectHandler(
        device_type="cisco_ios",
        host=host,
        port=port,
        username=username,
        password=password,
    )


def send_command(connection: BaseConnection, command: str) -> str:
    """Send a CLI command and return the output as a string."""
    return connection.send_command(command)
