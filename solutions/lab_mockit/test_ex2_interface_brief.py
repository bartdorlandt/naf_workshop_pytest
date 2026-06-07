from device_connector import send_command
from output_parser import parse_ip_interface_brief


class TestInterfaceBrief:
    def test_returns_list_of_interfaces(self, ios_device):
        output = send_command(ios_device, "show ip interface brief")
        interfaces = parse_ip_interface_brief(output)
        assert isinstance(interfaces, list)
        assert len(interfaces) > 0

    def test_interface_count(self, ios_device):
        output = send_command(ios_device, "show ip interface brief")
        interfaces = parse_ip_interface_brief(output)
        # Template has: Ethernet0/0, Ethernet0/0.11, Ethernet0/1, Ethernet0/2, Ethernet0/3, Loopback0
        assert len(interfaces) == 6

    def test_loopback_has_ip(self, ios_device):
        output = send_command(ios_device, "show ip interface brief")
        interfaces = parse_ip_interface_brief(output)
        loopback = next(i for i in interfaces if i["interface"] == "Loopback0")
        assert loopback["ip"] == "10.0.1.2"
        assert loopback["status"] == "up"
        assert loopback["protocol"] == "up"

    def test_down_interface_is_parsed(self, ios_device):
        output = send_command(ios_device, "show ip interface brief")
        interfaces = parse_ip_interface_brief(output)
        eth02 = next(i for i in interfaces if i["interface"] == "Ethernet0/2")
        assert eth02["status"] == "administratively"
        assert eth02["protocol"] == "down"

    def test_subinterface_has_ip(self, ios_device):
        output = send_command(ios_device, "show ip interface brief")
        interfaces = parse_ip_interface_brief(output)
        sub = next(i for i in interfaces if i["interface"] == "Ethernet0/0.11")
        assert sub["ip"] == "10.0.1.38"
