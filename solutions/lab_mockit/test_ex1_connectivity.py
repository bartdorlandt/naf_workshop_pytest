from device_connector import get_connection, send_command
from output_parser import parse_ios_version


class TestConnectivity:
    def test_can_connect_to_mock_device(self):
        conn = get_connection("127.0.0.1", 2222, "test", "test")
        assert conn.is_alive()
        conn.disconnect()

    def test_show_version_returns_output(self, ios_device):
        output = send_command(ios_device, "show version")
        assert len(output) > 0

    def test_show_version_contains_ios_xe(self, ios_device):
        output = send_command(ios_device, "show version")
        assert "IOS XE" in output

    def test_parsed_version_is_correct(self, ios_device):
        output = send_command(ios_device, "show version")
        result = parse_ios_version(output)
        assert result["version"] == "16.9.3"

    def test_parsed_hostname_is_correct(self, ios_device):
        output = send_command(ios_device, "show version")
        result = parse_ios_version(output)
        assert result["hostname"] == "csr1000v-1"

    def test_parsed_interface_count(self, ios_device):
        output = send_command(ios_device, "show version")
        result = parse_ios_version(output)
        assert result["interfaces"] == 3
