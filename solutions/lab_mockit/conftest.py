import netmiko
import pytest


@pytest.fixture(scope="session")
def ios_device() -> netmiko.BaseConnection:
    conn = netmiko.ConnectHandler(
        device_type="cisco_ios",
        host="127.0.0.1",
        port=2222,
        username="test",
        password="test",
    )
    yield conn
    conn.disconnect()
