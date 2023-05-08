def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert '"OK"' in response.text


def test_search_with_state(test_client):
    response = test_client.get("/berlin/search?q=Manch&state=GB&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
