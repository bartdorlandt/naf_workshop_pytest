import pytest
from unittest.mock import Mock

from mymodule import deploy_config


class TestRetryLogic:
    def test_succeeds_on_first_attempt(self, mocker):
        mock_device = Mock()
        mocker.patch("mymodule.connect", return_value=mock_device)

        deploy_config("switch01", "interface Ethernet1\n  shutdown")

        mock_device.commit_config.assert_called_once()

    def test_retries_on_transient_failure(self, mocker):
        mock_device = Mock()
        mock_connect = mocker.patch(
            "mymodule.connect",
            side_effect=[
                Exception("Connection failed"),
                Exception("Connection failed"),
                mock_device,
            ],
        )

        deploy_config("switch01", "interface Ethernet1\n  shutdown")

        assert mock_connect.call_count == 3
        mock_device.commit_config.assert_called_once()

    def test_raises_after_all_retries_exhausted(self, mocker):
        mocker.patch(
            "mymodule.connect",
            side_effect=Exception("Connection refused"),
        )

        with pytest.raises(RuntimeError, match="Failed after 3 attempts"):
            deploy_config("switch01", "interface Ethernet1\n  shutdown")
