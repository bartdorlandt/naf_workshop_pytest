import os
from datetime import datetime

from config_backup import generate_backup_filename, write_backup


class TestGenerateBackupFilename:
    def test_contains_hostname(self):
        ts = datetime(2024, 6, 8, 14, 30, 0)
        result = generate_backup_filename("spine-01", ts, "/var/backups")
        assert "spine-01" in result

    def test_contains_formatted_timestamp(self):
        ts = datetime(2024, 6, 8, 14, 30, 0)
        result = generate_backup_filename("spine-01", ts, "/var/backups")
        assert "20240608_143000" in result

    def test_uses_backup_dir(self):
        ts = datetime(2024, 6, 8, 14, 30, 0)
        result = generate_backup_filename("spine-01", ts, "/var/backups")
        assert result.startswith("/var/backups")

    def test_has_cfg_extension(self):
        ts = datetime(2024, 6, 8, 14, 30, 0)
        result = generate_backup_filename("spine-01", ts, "/var/backups")
        assert result.endswith(".cfg")

    def test_different_hostnames_produce_different_filenames(self):
        ts = datetime(2024, 6, 8, 14, 30, 0)
        f1 = generate_backup_filename("spine-01", ts, "/backups")
        f2 = generate_backup_filename("spine-02", ts, "/backups")
        assert f1 != f2


class TestWriteBackup:
    def test_writes_content_to_file(self, tmp_path):
        filename = str(tmp_path / "test.cfg")
        write_backup(filename, "interface Ethernet1\n")
        assert open(filename).read() == "interface Ethernet1\n"

    def test_creates_missing_directories(self, tmp_path):
        filename = str(tmp_path / "nested" / "dir" / "test.cfg")
        write_backup(filename, "content")
        assert os.path.exists(filename)
