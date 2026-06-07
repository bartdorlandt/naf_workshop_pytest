def test_config_file_exists(config_file):
    assert config_file.exists()


def test_config_file_has_hostname(config_file):
    assert "testdevice" in config_file.read_text()
