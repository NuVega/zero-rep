import pytest
import requests
from main import get_random_cat

class DummyResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data or []

    def json(self):
        return self._json

def test_successful_request(monkeypatch):
    def mock_get(*args, **kwargs):
        return DummyResponse(200, [{"url": "https://cdn2.thecatapi.com/images/abc.jpg"}])
    monkeypatch.setattr(requests, "get", mock_get)

    url = get_random_cat()
    assert url == "https://cdn2.thecatapi.com/images/abc.jpg"

def test_failed_request(monkeypatch):
    def mock_get(*args, **kwargs):
        return DummyResponse(404)
    monkeypatch.setattr(requests, "get", mock_get)

    url = get_random_cat()
    assert url is None