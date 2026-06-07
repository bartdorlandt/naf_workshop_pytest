import pytest


@pytest.fixture(autouse=True)
def default_api_url(monkeypatch):
    monkeypatch.setenv("API_URL", "https://api.example.com")
