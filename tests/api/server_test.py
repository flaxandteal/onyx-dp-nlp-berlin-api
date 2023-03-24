import pytest
from unittest.mock import patch, MagicMock


def test_health_check(test_client):
    response = test_client.get('/health')
    assert response.status_code == 200
    assert response.text == '"OK"'

def test_get_categories(test_client):
    response = test_client.get('/categories?query=test')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
