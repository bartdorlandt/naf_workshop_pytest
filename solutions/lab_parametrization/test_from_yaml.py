from pathlib import Path

import pytest
import yaml
from config_generator import select_driver


# Using Path(__file__).parent / "test_data.yaml" allows us to load the YAML file relative
# to the test file, making it more portable and easier to run from different locations."
def load_test_devices():
    data = yaml.safe_load((Path(__file__).parent / "test_data.yaml").read_text())
    return [pytest.param(d, id=d["hostname"]) for d in data["devices"]]


@pytest.mark.parametrize("device", load_test_devices())
def test_device_driver_selection(device):
    result = select_driver(device["vendor"])
    assert result == device["expected_driver"]
