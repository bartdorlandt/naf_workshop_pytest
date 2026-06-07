from inventory_client import transform_device_data


def make_raw_device(
    name="leaf-01", ip: str | None = "10.0.0.1/32", role="leaf", site="amsterdam"
):
    return {
        "name": name,
        "primary_ip": {"address": ip} if ip else None,
        "role": {"slug": role},
        "site": {"slug": site},
    }


class TestTransformDeviceData:
    def test_extracts_name(self):
        result = transform_device_data([make_raw_device(name="spine-01")])
        assert result[0]["name"] == "spine-01"

    def test_extracts_ip_without_prefix_length(self):
        result = transform_device_data([make_raw_device(ip="10.0.0.1/32")])
        assert result[0]["ip"] == "10.0.0.1"

    def test_ip_is_none_when_no_primary_ip(self):
        result = transform_device_data([make_raw_device(ip=None)])
        assert result[0]["ip"] is None

    def test_extracts_role(self):
        result = transform_device_data([make_raw_device(role="spine")])
        assert result[0]["role"] == "spine"

    def test_extracts_site(self):
        result = transform_device_data([make_raw_device(site="frankfurt")])
        assert result[0]["site"] == "frankfurt"

    def test_handles_multiple_devices(self):
        raw = [make_raw_device(name="leaf-01"), make_raw_device(name="leaf-02")]
        result = transform_device_data(raw)
        assert len(result) == 2
        assert result[0]["name"] == "leaf-01"
        assert result[1]["name"] == "leaf-02"

    def test_empty_list_returns_empty(self):
        assert transform_device_data([]) == []
