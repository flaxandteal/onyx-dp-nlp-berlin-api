from berlin import Location


def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert '"OK"' in response.text


def test_code_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get("/v1/berlin/code/UN-LOCODE-bg:blo")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "encoding": "UN-LOCODE",
        "id": "bg:blo",
        "key": "UN-LOCODE-bg:blo",
        "words": ["lyuliakovo"],
    }
    print(response.json)


def test_search_with_state_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get(
        "/v1/berlin/search?q=Lyuliakovo&state=BG&limit=2"
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    print(response.json)


def test_search_with_state(test_client):
    response = test_client.get("/v1/berlin/search?q=Manch&state=GB&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "matches": [{"encoding": "B", "id": "X", "key": "A", "words": ["Manchester"]}]
    }
