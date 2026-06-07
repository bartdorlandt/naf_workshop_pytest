from pathlib import Path
from typing import Any, Generator

import pytest


@pytest.fixture
def switch_config() -> dict[str, Any]:
    return {
        "hostname": "switch01",
        "vlans": [10, 20, 30],
        "interfaces": {
            "Ethernet1": {"mode": "access", "vlan": 10},
            "Ethernet2": {"mode": "trunk", "allowed_vlans": [10, 20, 30]},
        },
    }


@pytest.fixture
def config_file(tmp_path: Path) -> Generator[Path, None, None]:
    config = tmp_path / "device_config.yaml"
    config.write_text("""
hostname: testdevice
interfaces:
  - name: Ethernet1
    ip: 192.168.1.1/24
""")
    yield config


@pytest.fixture(scope="module")
def expensive_inventory() -> dict[str, list[str]]:
    print("\n>>> Loading inventory (expensive operation)")
    return {"devices": ["sw1", "sw2", "sw3"]}


@pytest.fixture
def device_list() -> list[str]:
    return ["switch01", "switch02", "router01"]


@pytest.fixture
def switches_only(device_list: list[str]) -> list[str]:
    return [d for d in device_list if d.startswith("switch")]


@pytest.fixture
def first_switch(switches_only: list[str]) -> str:
    return switches_only[0]
