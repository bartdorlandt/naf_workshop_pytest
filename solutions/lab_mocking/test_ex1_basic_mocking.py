from unittest.mock import Mock

from device_info import get_device_hostname, get_device_interfaces


class TestGetDeviceHostname:
    def test_returns_hostname_from_facts(self):
        mock_device = Mock()
        mock_device.get_facts.return_value = {"hostname": "switch01"}

        result = get_device_hostname(mock_device)

        assert result == "switch01"
        mock_device.get_facts.assert_called_once()

    def test_returns_unknown_when_hostname_missing(self):
        mock_device = Mock()
        mock_device.get_facts.return_value = {}

        result = get_device_hostname(mock_device)

        assert result == "unknown"


class TestGetDeviceInterfaces:
    def test_returns_interfaces_dict(self):
        mock_device = Mock()
        mock_device.get_interfaces.return_value = {
            "Ethernet1": {"is_up": True, "is_enabled": True},
            "Ethernet2": {"is_up": False, "is_enabled": True},
        }

        result = get_device_interfaces(mock_device)

        assert "Ethernet1" in result
        assert result["Ethernet1"]["is_up"] is True
        mock_device.get_interfaces.assert_called_once()
