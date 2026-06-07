import sqlite3

import pytest

from device_registry import add_device, build_device_record, get_devices_for_site


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE devices (hostname TEXT, ip_address TEXT, device_type TEXT, site TEXT)"
    )
    yield conn
    conn.close()


class TestBuildDeviceRecord:
    def test_returns_dict_for_valid_row(self):
        row = ("leaf-01", "10.0.0.1", "switch", "amsterdam")
        result = build_device_record(row)
        assert result == {
            "hostname": "leaf-01",
            "ip": "10.0.0.1",
            "type": "switch",
            "site": "amsterdam",
        }

    def test_returns_none_when_ip_is_empty(self):
        row = ("leaf-01", "", "switch", "amsterdam")
        assert build_device_record(row) is None

    def test_returns_none_when_ip_is_null(self):
        row = ("leaf-01", None, "switch", "amsterdam")
        assert build_device_record(row) is None


class TestAddDevice:
    def test_inserts_record(self, db):
        add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
        row = db.execute("SELECT * FROM devices").fetchone()
        assert row == ("leaf-01", "10.0.0.1", "switch", "amsterdam")

    def test_inserts_multiple_records(self, db):
        add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
        add_device(db, "leaf-02", "10.0.0.2", "switch", "amsterdam")
        rows = db.execute("SELECT * FROM devices").fetchall()
        assert len(rows) == 2


class TestGetDevicesForSite:
    def test_returns_devices_for_site(self, db):
        add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
        result = get_devices_for_site(db, "amsterdam")
        assert len(result) == 1
        assert result[0]["hostname"] == "leaf-01"

    def test_excludes_other_sites(self, db):
        add_device(db, "leaf-01", "10.0.0.1", "switch", "amsterdam")
        add_device(db, "spine-01", "10.1.0.1", "router", "frankfurt")
        result = get_devices_for_site(db, "amsterdam")
        assert all(d["site"] == "amsterdam" for d in result)

    def test_excludes_devices_without_ip(self, db):
        db.execute(
            "INSERT INTO devices VALUES ('ghost-01', NULL, 'switch', 'amsterdam')"
        )
        db.commit()
        result = get_devices_for_site(db, "amsterdam")
        assert result == []

    def test_returns_empty_for_unknown_site(self, db):
        assert get_devices_for_site(db, "nowhere") == []
