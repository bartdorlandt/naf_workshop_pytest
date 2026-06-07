from device_connector import send_command
from output_parser import parse_bgp_summary


class TestBgpSummary:
    def test_local_as_is_correct(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        assert result["local_as"] == 65000

    def test_router_id_is_correct(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        assert result["router_id"] == "10.0.0.0"

    def test_neighbor_count(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        assert len(result["neighbors"]) == 10

    def test_first_neighbor_remote_as(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        neighbor = next(n for n in result["neighbors"] if n["neighbor"] == "10.0.0.1")
        assert neighbor["remote_as"] == 65000

    def test_last_neighbor_is_idle(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        neighbor = next(n for n in result["neighbors"] if n["neighbor"] == "10.0.0.10")
        assert "Idle" in neighbor["state"]

    def test_neighbors_include_all_expected_ips(self, ios_device):
        output = send_command(ios_device, "show ip bgp summary")
        result = parse_bgp_summary(output)
        neighbor_ips = {n["neighbor"] for n in result["neighbors"]}
        expected = {f"10.0.0.{i}" for i in range(1, 11)}
        assert expected == neighbor_ips
