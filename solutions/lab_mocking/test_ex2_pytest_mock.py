from network_utils import get_device_from_api, list_devices_for_site


class TestGetDeviceFromApi:
    def test_returns_device_data(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"id": "123", "hostname": "switch01"}

        mock_get = mocker.patch("network_utils.requests.get")
        mock_get.return_value = mock_response

        result = get_device_from_api("123")

        assert result["hostname"] == "switch01"
        mock_get.assert_called_once_with("https://api.example.com/devices/123")

    def test_calls_raise_for_status(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {}
        mocker.patch("network_utils.requests.get", return_value=mock_response)

        get_device_from_api("123")

        mock_response.raise_for_status.assert_called_once()


class TestListDevicesForSite:
    def test_returns_results_for_site(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "results": [
                {"hostname": "sw1", "site": "amsterdam"},
                {"hostname": "sw2", "site": "amsterdam"},
            ]
        }
        mock_get = mocker.patch(
            "network_utils.requests.get", return_value=mock_response
        )

        result = list_devices_for_site("amsterdam")

        assert len(result) == 2
        mock_get.assert_called_once_with(
            "https://api.example.com/devices/", params={"site": "amsterdam"}
        )

    def test_returns_empty_list_when_no_results(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"results": []}
        mocker.patch("network_utils.requests.get", return_value=mock_response)

        result = list_devices_for_site("unknown-site")

        assert result == []
