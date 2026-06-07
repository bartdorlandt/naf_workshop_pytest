import pytest

from network_utils import get_device_from_api


class TestSimulatingFailures:
    def test_connection_timeout_raises(self, mocker):
        from socket import timeout

        mocker.patch(
            "network_utils.requests.get", side_effect=timeout("Connection timed out")
        )

        with pytest.raises(timeout):
            get_device_from_api("switch01")

    def test_http_error_propagates(self, mocker):
        import requests

        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mocker.patch("network_utils.requests.get", return_value=mock_response)

        with pytest.raises(requests.HTTPError):
            get_device_from_api("nonexistent")
