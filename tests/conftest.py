import pytest

BASE_URL = "http://127.0.0.1:5000"
@pytest.fixture
def api_url():
    return BASE_URL