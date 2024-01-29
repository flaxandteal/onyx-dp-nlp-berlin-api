

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert '"OK"' in response.text


def test_code_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get("/berlin/code/UN-LOCODE-bg:blo")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "encoding": "UN-LOCODE",
        "id": "bg:blo",
        "key": "UN-LOCODE-bg:blo",
        "names": ["lyuliakovo"],
        "words": ["lyuliakovo"],
        "codes": ["blo"],
        "state": ["bg", "bulgaria"],
        "subdiv": ["02", "burgas"],
    }
    print(response.json)


def test_search_with_state_with_berlin(test_client_with_berlin):
    response = test_client_with_berlin.get(
        "/berlin/search?q=Lyuliakovo&state=BG&limit=2"
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "matches": [{
            "encoding": "UN-LOCODE",
            "id": "bg:blo",
            "key": "UN-LOCODE-bg:blo",
            "names": ["lyuliakovo"],
            "words": ["lyuliakovo"],
            "codes": ["blo"],
            "state": ["bg", "bulgaria"],
            "subdiv": ["02", "burgas"],
        }]
    }
    print(response.json)


def test_search_with_state(test_client):
    response = test_client.get("/berlin/search?q=Manch&state=GB&limit=2")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json == {
        "matches": [{
            "encoding": "B",
            "id": "X",
            "key": "A",
            "names": ["manc"],
            "words": ["Manchester"],
            "codes": ["mnc"],
            "state": ["gb", "gb-nom"],
            "subdiv": ["mac", "gb-mac-name"],
        }]
    }
