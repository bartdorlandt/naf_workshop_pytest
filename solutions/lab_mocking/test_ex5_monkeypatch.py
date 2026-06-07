import pytest
import network_utils
from network_utils import get_api_url, get_device_from_api


class TestGetApiUrl:
    def test_returns_env_var_when_set(self, monkeypatch):
        monkeypatch.setenv("API_URL", "https://staging.example.com")
        assert get_api_url() == "https://staging.example.com"

    def test_returns_default_when_not_set(self, monkeypatch):
        monkeypatch.delenv("API_URL", raising=False)
        assert get_api_url() == "https://api.example.com"


class TestGetDeviceFromApiWithMonkeypatch:
    def test_uses_api_url_env_var(self, monkeypatch):
        monkeypatch.setenv("API_URL", "https://staging.example.com")

        mock_response = pytest.importorskip("unittest.mock").Mock()
        mock_response.json.return_value = {"id": "123", "hostname": "sw-staging"}
        monkeypatch.setattr(
            network_utils.requests, "get", lambda *a, **kw: mock_response
        )

        result = get_device_from_api("123")

        assert result["hostname"] == "sw-staging"

    def test_setattr_replaces_requests_get(self, monkeypatch):
        from unittest.mock import Mock

        mock_response = Mock()
        mock_response.json.return_value = {"id": "42", "hostname": "switch01"}

        calls = []

        def fake_get(url, **kwargs):
            calls.append(url)
            return mock_response

        monkeypatch.setattr(network_utils.requests, "get", fake_get)

        result = get_device_from_api("42")

        assert result["hostname"] == "switch01"
        assert calls[0].endswith("/devices/42")
